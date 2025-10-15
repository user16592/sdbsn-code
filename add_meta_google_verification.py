import os
import re

META_TAG = '<meta name="google-site-verification" content="w1WK4nbTuDnvjHJNmmbSghgSV8akwX1GuZ9haPwgoK4" />'


def insert_or_replace_meta(content: str) -> (str, bool):
    """Ensure the META_TAG exists in the <head> of the HTML content.
    If an existing google-site-verification meta tag is present, replace it.
    Otherwise insert the META_TAG into <head> (or create a <head> if missing).
    Returns (new_content, changed).
    """
    changed = False

    # Pattern to match any google-site-verification meta tag
    meta_re = re.compile(r'<meta[^>]+name=["\']google-site-verification["\'][^>]*>', re.IGNORECASE)

    # If a meta tag exists, replace all occurrences with the desired META_TAG
    if meta_re.search(content):
        new_content = meta_re.sub(META_TAG, content)
        if new_content != content:
            return new_content, True
        return content, False

    # If there's an opening <head> tag, insert right after it
    head_open_re = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
    if head_open_re.search(content):
        new_content = head_open_re.sub(r"\1\n    " + META_TAG, content, count=1)
        return new_content, True

    # If no <head> but an <html> exists, create a head block after <html...>
    html_open_re = re.compile(r'(<html[^>]*>)', re.IGNORECASE)
    if html_open_re.search(content):
        insertion = "\n<head>\n    " + META_TAG + "\n</head>\n"
        new_content = html_open_re.sub(r"\1" + insertion, content, count=1)
        return new_content, True

    # As a last resort, insert the meta at the top of the file
    new_content = META_TAG + "\n" + content
    return new_content, True


def process_file(path: str) -> bool:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[SKIP] Could not read {path}: {e}")
        return False

    new_content, changed = insert_or_replace_meta(content)
    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[UPDATED] {path}")
            return True
        except Exception as e:
            print(f"[ERROR] Could not write {path}: {e}")
            return False
    else:
        print(f"[SKIP] Meta already present in {path}")
        return False


def main():
    root_dir = '.'
    updated = 0
    total = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            if name.lower().endswith(('.html', '.htm')):
                total += 1
                path = os.path.join(dirpath, name)
                if process_file(path):
                    updated += 1

    print(f"Done. Processed {total} html files, updated {updated} files.")


if __name__ == '__main__':
    main()
