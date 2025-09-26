from Config.Util import *
from Config.Config import *
try:
    import base64
    import binascii
    from PIL import Image
    import os
except Exception as e:
    ErrorModule(e)

Title("Steganography Tool")

try:
    def hide_text_in_image(image_path, text, output_path):
        try:
            img = Image.open(image_path)
            encoded_text = text.encode('utf-8')
            
            # Convert text to binary
            binary_text = ''.join(format(byte, '08b') for byte in encoded_text)
            binary_text += '1111111111111110'  # Delimiter
            
            pixels = list(img.getdata())
            new_pixels = []
            
            text_index = 0
            for pixel in pixels:
                if text_index < len(binary_text):
                    # Modify LSB of red channel
                    r, g, b = pixel[:3]
                    r = (r & 0xFE) | int(binary_text[text_index])
                    new_pixels.append((r, g, b) + pixel[3:])
                    text_index += 1
                else:
                    new_pixels.append(pixel)
            
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(new_pixels)
            new_img.save(output_path)
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Text hidden in image: {white}{output_path}")
            return True
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error hiding text: {white}{e}")
            return False

    def extract_text_from_image(image_path):
        try:
            img = Image.open(image_path)
            pixels = list(img.getdata())
            
            binary_text = ''
            for pixel in pixels:
                r = pixel[0]
                binary_text += str(r & 1)
            
            # Find delimiter
            delimiter = '1111111111111110'
            delimiter_index = binary_text.find(delimiter)
            
            if delimiter_index != -1:
                binary_text = binary_text[:delimiter_index]
                
                # Convert binary to text
                text = ''
                for i in range(0, len(binary_text), 8):
                    byte = binary_text[i:i+8]
                    if len(byte) == 8:
                        text += chr(int(byte, 2))
                
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Extracted text: {white}{text}")
                return text
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No hidden text found")
                return None
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error extracting text: {white}{e}")
            return None

    def encode_file_base64(file_path):
        try:
            with open(file_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            
            output_file = os.path.join(tool_path, "1-Output", "Steganography", f"encoded_{os.path.basename(file_path)}.txt")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(encoded)
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File encoded to: {white}{output_file}")
            return True
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error encoding file: {white}{e}")
            return False

    def decode_file_base64(encoded_file_path, output_path):
        try:
            with open(encoded_file_path, 'r') as f:
                encoded_data = f.read()
            
            decoded_data = base64.b64decode(encoded_data)
            
            with open(output_path, 'wb') as f:
                f.write(decoded_data)
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File decoded to: {white}{output_path}")
            return True
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error decoding file: {white}{e}")
            return False

    Slow(f"""{virus_banner}
 {BEFORE}01{AFTER}{white} Hide text in image
 {BEFORE}02{AFTER}{white} Extract text from image
 {BEFORE}03{AFTER}{white} Encode file to Base64
 {BEFORE}04{AFTER}{white} Decode Base64 to file
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Operation -> {reset}")
    
    if choice in ['1', '01']:
        image_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Image path -> {reset}")
        text = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Text to hide -> {reset}")
        output_path = os.path.join(tool_path, "1-Output", "Steganography", f"hidden_{os.path.basename(image_path)}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        hide_text_in_image(image_path, text, output_path)
        
    elif choice in ['2', '02']:
        image_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Image path -> {reset}")
        extract_text_from_image(image_path)
        
    elif choice in ['3', '03']:
        file_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} File path -> {reset}")
        encode_file_base64(file_path)
        
    elif choice in ['4', '04']:
        encoded_file = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Encoded file path -> {reset}")
        output_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Output file path -> {reset}")
        decode_file_base64(encoded_file, output_path)
        
    else:
        ErrorChoice()

    Continue()
    Reset()
except Exception as e:
    Error(e)