import json
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'assets', 'data', 'projects.json')
TEMPLATE_PATH = os.path.join(ROOT, 'tools', 'project-template.html')
IMAGES_DIR = os.path.join(ROOT, 'assets', 'img', 'projects')


def get_image_size(prefix, index):
    path = os.path.join(IMAGES_DIR, f'{prefix}-{index:02d}.webp')
    if not os.path.exists(path):
        raise FileNotFoundError(f'Image not found: {path}')
    with Image.open(path) as img:
        return img.size


def build_gallery(project):
    lines = []
    prefix = project['slug']
    for i in range(1, project['images'] + 1):
        width, height = get_image_size(prefix, i)
        thumb = f'assets/img/projects/{prefix}-{i:02d}.webp'
        alt = f'{project["title"]} — скриншот {i}'
        lines.append(
            f'                    <a href="{thumb}" '
            f'data-pswp-width="{width}" data-pswp-height="{height}" '
            f'target="_blank" class="project-gallery-item">\n'
            f'                        <img src="{thumb}" alt="{alt}" loading="lazy" width="{width}" height="{height}">\n'
            f'                        <span class="project-gallery-zoom"><i class="fas fa-magnifying-glass-plus"></i></span>\n'
            f'                    </a>'
        )
    return '\n'.join(lines)


def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        projects = json.load(f)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    for project in projects:
        tags_html = '\n                    '.join(
            f'<span>{tag}</span>' for tag in project['tags']
        )

        content = template
        content = content.replace('{{SLUG}}', project['slug'])
        content = content.replace('{{TITLE}}', project['title'])
        content = content.replace('{{DESCRIPTION}}', project['description'])
        content = content.replace('{{TASK}}', project['task'])
        content = content.replace('{{SOLUTION}}', project['solution'])
        content = content.replace('{{TAGS}}', tags_html)
        content = content.replace('{{GALLERY}}', build_gallery(project))

        output_path = os.path.join(ROOT, f'project-{project["slug"]}.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Generated: {os.path.basename(output_path)}')


if __name__ == '__main__':
    main()
