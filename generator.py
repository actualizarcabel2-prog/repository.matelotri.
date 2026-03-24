import os, zipfile, hashlib

def build_repo():
    print("[Matelotri Generator] Construyendo el repositorio completamente limpio...")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    addons_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'
    
    # Carpetas que son addons
    folders = ['repository.matelotri', 'plugin.program.matelotriwizard']
    
    for addon in folders:
        addon_path = os.path.join(root_dir, addon)
        if not os.path.isdir(addon_path): continue
        
        # 1. Empaqueta el ZIP dinámicamente simulando v1.0.0
        zip_name = f"{addon}-1.0.0.zip"
        zip_path = os.path.join(addon_path, zip_name)
        
        # Omitimos el zip antiguo si existe
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirname, subdirs, files in os.walk(addon_path):
                for f in files:
                    if f.endswith('.zip') or f.endswith('.pyc'): continue
                    abs_p = os.path.join(dirname, f)
                    # Añadir al zip con la estructura interna adecuada (carpeta_base/archivo)
                    arcname = os.path.join(addon, os.path.relpath(abs_p, addon_path))
                    zf.write(abs_p, arcname)
        print(f"Empaquetado listo: {zip_path}")

        # 2. Leer addon.xml e inyectarlo en addons.xml
        xml_file = os.path.join(addon_path, 'addon.xml')
        if os.path.exists(xml_file):
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '?>' in content:
                content = content.split('?>', 1)[1].strip()
            addons_xml += content + '\n'
            print(f"Sumando metadata de {addon}...")

    addons_xml += '</addons>\n'
    
    # Escribimos addons.xml
    with open('addons.xml', 'w', encoding='utf-8') as f:
        f.write(addons_xml)
        
    # Escribimos md5
    m = hashlib.md5()
    m.update(addons_xml.encode('utf-8'))
    with open('addons.xml.md5', 'w', encoding='utf-8') as f:
        f.write(m.hexdigest())

    print("[Matelotri Generator] Todo construido y actualizado correctamente.")

if __name__ == '__main__':
    build_repo()
