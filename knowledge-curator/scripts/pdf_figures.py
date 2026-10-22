import argparse
import hashlib
import json
import math
from pathlib import Path

import pymupdf


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_outputs(paths, force):
    for path in paths:
        if path.exists() and not force:
            raise ValueError(f"Output already exists: {path}; use --force to replace it")
        if path.exists() and not path.is_file():
            raise ValueError(f"Output is not a file: {path}")
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def inspect_pdf(document, source, output, force):
    text_path = output / "paper.txt"
    layout_path = output / "pages.json"
    check_outputs([text_path, layout_path], force)
    pages = []
    text_parts = []
    for page in document:
        page_text = page.get_text(sort=True)
        text_parts.append(f"===== PDF PAGE {page.number + 1} =====\n{page_text}")
        pages.append({
            "page": page.number + 1,
            "size_pt": [page.rect.width, page.rect.height],
            "rotation": page.rotation,
            "has_text": bool(page_text.strip()),
            "embedded_image_count": len(page.get_images()),
            "vector_path_count": len(page.get_drawings()),
            "text_blocks_unrotated_pt": [
                {"bbox": list(block[:4]), "text": block[4]}
                for block in page.get_text("blocks") if block[6] == 0
            ],
        })
    text_path.write_text("\n".join(text_parts), encoding="utf-8")
    write_json(layout_path, {
        "source_pdf": str(source),
        "source_sha256": sha256_file(source),
        "page_count": len(document),
        "pages": pages,
        "note": "Image/path counts do not identify figures. Inspect rendered pages; zero images does not mean no figures.",
    })
    return {"text": str(text_path), "layout": str(layout_path), "pages": len(document)}


def load_page(document, page_number):
    if not 1 <= page_number <= len(document):
        raise ValueError(f"Page must be between 1 and {len(document)} (1-based)")
    return document[page_number - 1]


def validate_clip(values):
    left, top, right, bottom = values
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Clip coordinates must be finite")
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise ValueError("Clip must satisfy 0 <= left < right <= 1 and 0 <= top < bottom <= 1")
    return left, top, right, bottom


def render_page(document, args):
    page = load_page(document, args.page)
    if args.output.suffix.lower() != ".png":
        raise ValueError("Output must end in .png")
    if not 72 <= args.dpi <= 600:
        raise ValueError("DPI must be between 72 and 600")
    metadata_path = args.output.with_suffix(".json")
    outputs = [args.output, metadata_path] if args.command == "extract" else [args.output]
    clip = page.rect
    if args.command == "extract":
        left, top, right, bottom = validate_clip(args.clip)
        clip = pymupdf.Rect(
            page.rect.x0 + left * page.rect.width,
            page.rect.y0 + top * page.rect.height,
            page.rect.x0 + right * page.rect.width,
            page.rect.y0 + bottom * page.rect.height,
        )
    check_outputs(outputs, args.force)
    pixmap = page.get_pixmap(dpi=args.dpi, clip=clip, colorspace=pymupdf.csRGB, alpha=False)
    if pixmap.width == 0 or pixmap.height == 0:
        raise ValueError("Crop produced an empty image")
    pixmap.save(str(args.output))
    result = {"image": str(args.output), "pixels": [pixmap.width, pixmap.height]}
    if args.command == "extract":
        write_json(metadata_path, {
            "source_pdf": str(args.pdf),
            "source_sha256": sha256_file(args.pdf),
            "pdf_page": args.page,
            "figure": args.figure,
            "caption": args.caption,
            "clip_normalized": list(args.clip),
            "clip_display_pt": list(clip),
            "page_rotation": page.rotation,
            "coordinate_system": "displayed page, top-left origin; x right, y down",
            "dpi": args.dpi,
            "pixels": [pixmap.width, pixmap.height],
            "image": args.output.name,
            "image_sha256": sha256_file(args.output),
            "method": "original PDF page region rendered by PyMuPDF; no redrawing or OCR",
            "pymupdf_version": pymupdf.VersionBind,
        })
        result["provenance"] = str(metadata_path)
    return result


def main():
    parser = argparse.ArgumentParser(description="Inspect a PDF and export original figure regions, including vector graphics.")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("inspect", "render", "extract"):
        subparser = commands.add_parser(command)
        subparser.add_argument("--pdf", type=Path, required=True)
        subparser.add_argument("--output", type=Path, required=True)
        subparser.add_argument("--force", action="store_true")
        if command != "inspect":
            subparser.add_argument("--page", type=int, required=True, help="1-based PDF page number")
            subparser.add_argument("--dpi", type=int, default=144 if command == "render" else 300)
        if command == "extract":
            subparser.add_argument("--clip", type=float, nargs=4, required=True, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"), help="Fractions of displayed page width/height, from 0 to 1")
            subparser.add_argument("--figure", required=True, help="Original figure label, e.g. Figure 1")
            subparser.add_argument("--caption", default="", help="Verified caption or concise source description")
    args = parser.parse_args()
    args.pdf = args.pdf.resolve()
    args.output = args.output.resolve()
    try:
        output_paths = [args.output, args.output.with_suffix(".json")]
        if args.command == "inspect":
            output_paths = [args.output / "paper.txt", args.output / "pages.json"]
        if args.pdf in output_paths:
            raise ValueError("Output cannot replace the source PDF")
        with pymupdf.open(args.pdf) as document:
            if not document.is_pdf:
                raise ValueError("Input must be a PDF")
            if document.needs_pass:
                raise ValueError("PDF requires a password; provide an unlocked copy")
            if args.command == "inspect":
                result = inspect_pdf(document, args.pdf, args.output, args.force)
            else:
                result = render_page(document, args)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"{ascii(str(error))}\n")
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
