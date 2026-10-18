"""Build Fashion's current printable editions and post pack from the selected text.

Requires requirements-production.txt. Use --video --ffmpeg PATH for both cuts.
Supplied reference packages and the previous proof filenames are preserved.
"""
import argparse
import html
import json
import math
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import pymupdf as fitz
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Image as PDFImage

from common import ROOT, paragraphs, read_json, write_json
from build_products import card, save, film_plan, render_film

FOLDER = ROOT / 'chapters/fashion'
META = read_json(FOLDER / 'chapter.json')
URL = read_json(ROOT / 'book.json')['public_url'] + META['canonical_path']


def write(relative, text):
    path = FOLDER / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def scene_crops():
    records = []
    for index in range(1, 7):
        source = FOLDER / f'artwork/scenes/scene_{index:02d}.jpg'
        image = Image.open(source)
        assert image.size == (1500, 1125)
        box = (50, 50, 1450, 845)  # Art only: omit the baked-in label panel.
        target = f'artwork/exports/detail-{index:02d}.jpg'
        save(image.crop(box), FOLDER / target)
        records.append({'path': target, 'source': source.relative_to(FOLDER).as_posix(), 'crop_pixels': list(box), 'native_size': [1400, 795], 'provenance': 'Supplied illustration crop; source detail is limited by the original master, not the export size.'})
    write_json(FOLDER / 'artwork/exports/crops.json', records)


def print_pdf(filename, size, illustrated):
    width, height = size
    margin = 15 * mm if illustrated else 20 * mm
    body_width = width - 2 * margin
    palette = META['palette']
    def furniture(canvas, doc):
        canvas.setFillColor(HexColor(palette['dark']))
        canvas.setFont('Label', 7)
        canvas.drawString(margin, height - 10 * mm, '.json / FASHION / 02')
        canvas.drawRightString(width - margin, height - 10 * mm, 'JASON, UNDER REVISION')
        canvas.setStrokeColor(HexColor('#BBBBBB'))
        canvas.line(margin, 12 * mm, width - margin, 12 * mm)
        canvas.setFont('Label', 6.5)
        canvas.drawString(margin, 8 * mm, 'AUTHOR REVISION / 17 OCTOBER 2026')
        canvas.drawRightString(width - margin, 8 * mm, str(doc.page))
    style = ParagraphStyle('FashionBody', fontName='Chapter', fontSize=11, leading=16.2,
                           textColor=HexColor('#17251F'), spaceAfter=12, allowWidows=0, allowOrphans=0, splitLongWords=False)
    title = ParagraphStyle('FashionTitle', parent=style, fontName='ChapterItalic', fontSize=34, leading=39, spaceAfter=18)
    label = ParagraphStyle('FashionLabel', parent=style, fontName='Label', fontSize=8, leading=12)
    doc = SimpleDocTemplate(str(FOLDER / 'book' / filename), pagesize=size, leftMargin=margin, rightMargin=margin,
                            topMargin=18 * mm, bottomMargin=18 * mm, title='Fashion — Jason — 17 October 2026', author='Jason')
    flow = []
    if illustrated:
        image = Image.open(FOLDER / 'artwork/source/02_BOOK_POSTER.png')
        art_height = min(height - 48 * mm, body_width * image.height / image.width)
        art_width = art_height * image.width / image.height
        flow.extend([PDFImage(str(FOLDER / 'artwork/source/02_BOOK_POSTER.png'), width=art_width, height=art_height),
                     Spacer(1, 8), Paragraph('Fashion / Jason', label), PageBreak()])
    else:
        flow.extend([Paragraph('Fashion', title), Paragraph('Jason / Chapter 02', label), Spacer(1, 12)])
    prose = paragraphs(FOLDER / META['canonical_text'])
    for index, text in enumerate(prose):
        if index == len(prose) - 2:
            flow.append(KeepTogether([Paragraph(html.escape(p), style) for p in prose[-2:]]))
            break
        flow.append(Paragraph(html.escape(text), style))
        if illustrated and index in [1, 4, 7]:
            scene_index = {1: 1, 4: 3, 7: 5}[index]
            image_path = FOLDER / f'artwork/exports/detail-{scene_index:02d}.jpg'
            image_width = min(body_width, 92 * mm)
            image_height = image_width * 795 / 1400
            flow.extend([Spacer(1, 2), PDFImage(str(image_path), width=image_width, height=image_height), Spacer(1, 12)])
        if illustrated and index in [1, 2, 4, 6, 7]:
            flow.append(PageBreak())
    if illustrated:
        flow.extend([PageBreak(), Paragraph('Về ấn bản này', title),
                     Paragraph('Fashion / Chương 02 / Jason', label), Spacer(1, 16),
                     Paragraph('Bản tác giả cập nhật ngày 17/10/2026. Toàn bộ câu chữ, cách viết và chữ ký được giữ nguyên; chỉ chuẩn hóa khoảng cách giữa các đoạn.', style),
                     Paragraph('Minh họa từ bộ Fashion v02 do tác giả cung cấp. Những hình ảnh trong căn phòng là minh họa ý niệm, không phải ảnh tư liệu của tác giả.', style),
                     Spacer(1, 14), PDFImage(str(FOLDER / 'artwork/exports/detail-06.jpg'), width=body_width, height=body_width * 795 / 1400),
                     Spacer(1, 16), Paragraph('Đọc, khám phá và xem lịch sử phiên bản:', label),
                     Paragraph(f'<link href="{URL}">{URL}</link>', label)])
    doc.build(flow, onFirstPage=furniture, onLaterPages=furniture)
    return FOLDER / 'book' / filename


def booklet(source):
    original = fitz.open(source)
    count = math.ceil(len(original) / 4) * 4
    padded = fitz.open()
    padded.insert_pdf(original)
    while len(padded) < count:
        padded.new_page(width=A5[0], height=A5[1])
    output = fitz.open()
    width, height = A4[1], A4[0]
    order = []
    for sheet in range(count // 4):
        pairs = [(count - 1 - 2 * sheet, 2 * sheet), (2 * sheet + 1, count - 2 - 2 * sheet)]
        for pair in pairs:
            page = output.new_page(width=width, height=height)
            for side, index in enumerate(pair):
                if index < len(original):
                    page.show_pdf_page(fitz.Rect(side * width / 2, 0, (side + 1) * width / 2, height), padded, index)
            order.append([index + 1 if index < len(original) else None for index in pair])
    output.set_metadata({'title': 'Fashion — A4 duplex booklet', 'author': 'Jason', 'subject': 'Already imposed: print A4 landscape, actual size, duplex short edge; do not impose again.'})
    output.save(FOLDER / 'book/Fashion-A4-booklet.pdf', garbage=4, deflate=True)
    write_json(FOLDER / 'book/BOOKLET_ORDER.json', {'source': source.name, 'source_pages': len(original), 'padded_pages': count, 'sheets': count // 4, 'printed_sides': order, 'null_page': 'intentional blank padding'})


def social(recipe):
    alt = []
    for index, item in enumerate(recipe['publish_media']['carousel'], 1):
        image = card(META, Image.open(FOLDER / item['scene']), item['text'], number=f'{index:02d}', scene_fit='contain')
        target = f'social/instagram/slide-{index:02d}.jpg'
        save(image, FOLDER / target)
        alt.append({'file': target, 'alt': item['alt'], 'text': item['text']})
        # Keep earlier public download names useful, while immutable originals remain in references/.
        save(image, FOLDER / f'social/instagram/slide_{index:02d}_3x4.jpg')
    for index, item in enumerate(recipe['stories'], 1):
        target = f'social/instagram/story-{index:02d}.jpg'
        save(card(META, Image.open(FOLDER / item['scene']), item['text'], (1080, 1920), number=f'S{index:02d}', scene_fit='contain'), FOLDER / target)
        alt.append({'file': target, 'alt': item['alt'], 'text': item['text']})
    hero = Image.open(FOLDER / 'artwork/source/05_WIDE_HERO.png')
    covers = [('instagram/feed_4x5.jpg', (1080, 1350)), ('instagram/square_1x1.jpg', (1080, 1080)),
              ('tiktok/cover.jpg', (1080, 1920)), ('facebook_post_1600x900.jpg', (1600, 900)), ('youtube_thumbnail_1280x720.jpg', (1280, 720))]
    for relative, size in covers:
        save(card(META, hero, 'Fashion', size, cover_card=True, scene_fit='contain'), FOLDER / 'social' / relative)
        alt.append({'file': 'social/' + relative, 'alt': 'Fashion / Chapter 02. Minh họa căn phòng xanh, ánh trời hồng và tủ quần áo; không phải ảnh tư liệu.'})
    write_json(FOLDER / 'social/alt-text.json', alt)
    write_json(FOLDER / 'social/instagram/alt-text.json', alt[:5])
    thumbs = []
    for item in alt:
        image = Image.open(FOLDER / item['file'])
        image.thumbnail((240, 330))
        thumbs.append(image.copy())
    sheet = Image.new('RGB', (5 * 260, math.ceil(len(thumbs) / 5) * 360), '#F5EBD8')
    for index, image in enumerate(thumbs):
        sheet.paste(image, (index % 5 * 260 + (260 - image.width) // 2, index // 5 * 360 + 10))
    save(sheet, FOLDER / 'previews/social-current.jpg')


def pdf_previews():
    report = []
    for filename in ['Fashion-A5-print.pdf', 'Fashion-A4-ink-saving.pdf', 'Fashion-A4-booklet.pdf']:
        document = fitz.open(FOLDER / 'book' / filename)
        thumbs = []
        for page in document:
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            image.thumbnail((290, 410))
            thumbs.append(image)
        sheet = Image.new('RGB', (min(4, len(thumbs)) * 310, math.ceil(len(thumbs) / 4) * 435), '#DDD8CF')
        for index, image in enumerate(thumbs):
            sheet.paste(image, (index % 4 * 310 + 10, index // 4 * 435 + 10))
        save(sheet, FOLDER / 'previews' / (Path(filename).stem + '.jpg'))
        report.append({'file': 'book/' + filename, 'pages': len(document), 'page_mm': [round(document[0].rect.width / mm, 2), round(document[0].rect.height / mm, 2)]})
    write_json(FOLDER / 'book/PRINT_FILES.json', report)


def package_products():
    with ZipFile(FOLDER / 'book/Fashion-print-pack.zip', 'w', ZIP_DEFLATED) as bundle:
        for name in ['Fashion-A5-print.pdf', 'Fashion-A4-ink-saving.pdf', 'Fashion-A4-booklet.pdf', 'PRINT_GUIDE.md', 'BOOKLET_ORDER.json']:
            bundle.write(FOLDER / 'book' / name, name)
    with ZipFile(FOLDER / 'social/Fashion-social-pack.zip', 'w', ZIP_DEFLATED) as bundle:
        for path in sorted((FOLDER / 'social').rglob('*')):
            if path.is_file() and path.suffix != '.zip':
                bundle.write(path, path.relative_to(FOLDER))
        for name in ['discovery-9x16', 'essay-16x9']:
            for extension in ['mp4', 'srt', 'vtt']:
                bundle.write(FOLDER / f'video/{name}.{extension}', f'video/{name}.{extension}')
            bundle.write(FOLDER / f'audio/{name}-script.md', f'audio/{name}-script.md')
        bundle.write(FOLDER / 'video/STORYBOARD.md', 'video/STORYBOARD.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', action='store_true')
    parser.add_argument('--ffmpeg', default='ffmpeg')
    args = parser.parse_args()
    recipe = read_json(FOLDER / 'production.json')
    manuscript = (FOLDER / META['canonical_text']).read_text(encoding='utf-8')
    for item in recipe['publish_media']['carousel'] + recipe['stories']:
        assert item['text'] in manuscript, 'Excerpt differs from current author text'
    for film in recipe['films']:
        assert all(segment['text'] in manuscript for segment in film['segments'])
    scene_crops()
    a5 = print_pdf('Fashion-A5-print.pdf', A5, True)
    print_pdf('Fashion-A4-ink-saving.pdf', A4, False)
    booklet(a5)
    pdf_previews()
    social(recipe)
    variants = film_plan(FOLDER, META, [], [])
    if args.video:
        for variant in variants:
            render_film(FOLDER, META, variant, args.ffmpeg)
    for relative, text in recipe['copy'].items():
        write(relative, text.replace('{chapter_url}', URL))
    write('video/NARRATION_DRAFT.md', '# Fashion — current recording handoff\n\nFull manuscript: ../audio/reading-script.md. Exact short-cut excerpts: ../audio/discovery-9x16-script.md and ../audio/essay-16x9-script.md.\n\nThese replace the earlier paraphrased 60-second draft, preserved in references/fashion-v02/video/NARRATION_DRAFT.md. Record naturally, then retime the cut and generate speech subtitles from the recording. Current SRT/VTT describe on-screen text only.')
    package_products()
    print('Built current Fashion print editions, social pack and recording handoff.')


if __name__ == '__main__':
    main()
