import yaml
import re
import os

def _render_resource_list(items):
    lines = ['            <ul class="resource-list">']
    for item in items:
        link_html = ''
        if 'link' in item:
            link_html = f'''                <a href="{item['link']}" class="resource-link" target="_blank" title="Open Link">
                  <img src="assets/link.svg" alt="Link" />
                </a>'''

        item_html = f'''              <li>
                <span class="resource-name">{item['name']}</span>
                {link_html}
              </li>'''
        lines.append(item_html)
    lines.append('            </ul>')
    return '\n'.join(lines)


def generate_html_section(categories, intro_text):
    lines = [f'          <p>{intro_text}</p>']
    for cat in categories:
        lines.append('')
        lines.append('          <div class="bookshelf-category">')
        lines.append(f'            <h3>{cat["category"]}</h3>')
        groups = cat.get('groups')
        if groups:
            for group in groups:
                lines.append('')
                lines.append(f'            <h4>{group["name"]}</h4>')
                lines.append(_render_resource_list(group.get('items', [])))
        else:
            lines.append(_render_resource_list(cat.get('items', [])))
        lines.append('          </div>')
    return '\n'.join(lines)


def generate_project_cards(projects):
    lines = []
    lines.append('          <div class="projects-grid">')
    for project in projects:
        card_lines = ['            <div class="project-card">']
        card_lines.append('              <div class="project-card-image">')
        fit_cls = ' img-cover' if project.get('image_fit') == 'cover' else ''
        card_lines.append('                <img src="' + project['image'] + '" alt="' + project['name'] + '" class="project-card-img' + fit_cls + '" />')
        card_lines.append('              </div>')
        card_lines.append('              <div class="project-card-body">')
        card_lines.append('                <h3 class="project-card-title">' + project['name'] + '</h3>')
        card_lines.append('                <p class="project-card-desc">' + project['description'] + '</p>')
        card_lines.append('                <div class="project-card-footer">')
        card_lines.append('                  <span class="project-card-lang">' + project['language'] + '</span>')
        card_lines.append('                  <div class="project-card-links">')
        card_lines.append('                    <a href="' + project['github'] + '" class="project-link" target="_blank">GitHub</a>')
        if 'demo' in project and project['demo']:
            card_lines.append('                    <a href="' + project['demo'] + '" class="project-link project-link-demo" target="_blank">Demo</a>')
        card_lines.append('                  </div>')
        card_lines.append('                </div>')
        card_lines.append('              </div>')
        card_lines.append('            </div>')
        lines.extend(card_lines)
    lines.append('          </div>')
    return '\n'.join(lines)

def update_file(file_path, new_content):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}: file not found")
        return

    with open(file_path, 'r') as f:
        html = f.read()

    pattern = r'(<!-- CONTENT_START -->).*?(<!-- CONTENT_END -->)'
    replacement = f'\\1\n{new_content}\n          \\2'
    
    updated_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    with open(file_path, 'w') as f:
        f.write(updated_html)
    print(f"Successfully updated {file_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data.yaml')
    public_dir = os.path.join(os.path.dirname(script_dir), 'public')

    with open(data_path, 'r') as f:
        data = yaml.safe_load(f)

    # Update Bookshelf
    if 'bookshelf' in data:
        books_html = generate_html_section(data['bookshelf'], "A collection of books and papers I've read.")
        update_file(os.path.join(public_dir, 'bookshelf.html'), books_html)

    # Update Courseshelf
    if 'courseshelf' in data:
        courses_html = generate_html_section(data['courseshelf'], "A collection of courses I've studied.")
        update_file(os.path.join(public_dir, 'courseshelf.html'), courses_html)

    # Update Projects
    if 'projects' in data:
        projects_html = generate_project_cards(data['projects'])
        update_file(os.path.join(public_dir, 'projects.html'), projects_html)

if __name__ == "__main__":
    main()
