import os
from PIL import Image


def resize_and_convert_images(input_folder, output_folder, target_size=(250, 250), output_format="PNG"):
    # Nastavení cesty ke složce "New/Logos"
    output_folder = os.path.join(output_folder)

    # Vytvoření výstupní složky "New/Logos", pokud neexistuje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    # Procházení souborů ve složce
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        try:
            with Image.open(file_path) as img:
                # Převod do formátu RGBA (pro průhlednost)
                img = img.convert("RGBA")

                # Zachování poměru stran a změna velikosti
                img.thumbnail(target_size)

                # Vytvoření nového obrázku s průhledným pozadím o požadované velikosti
                new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))

                # Výpočet pozice pro zarovnání obrázku na střed
                paste_position = (
                    (target_size[0] - img.size[0]) // 2,
                    (target_size[1] - img.size[1]) // 2
                )

                # Vložení zmenšeného obrázku na průhledné pozadí
                new_img.paste(img, paste_position)

                # Uložení obrázku ve formátu PNG do výstupní složky
                base_name = os.path.splitext(filename)[0]  # Získání názvu souboru bez přípony
                output_path = os.path.join(output_folder, f"{base_name}.{output_format.lower()}")
                new_img.save(output_path, output_format)
                print(f"Processed and saved: {output_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


# Příklad použití:
if __name__ == "__main__":
    input_folder = "../AppFiles/Data/Test"  # Zadej cestu ke vstupní složce
    output_folder = "Generated Logos and Flags"  # Zadej cestu k výstupní složce (bude obsahovat New/Logos)
    resize_and_convert_images(input_folder, output_folder)
