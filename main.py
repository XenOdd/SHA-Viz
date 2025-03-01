import pygame
import pygame.freetype
import sys
import math
from typing import List, Tuple, Dict, Any, Optional

# Configuration
CONFIG = {
    "width": 1200,
    "height": 800,
    "bg_color": (240, 240, 240),
    "text_color": (20, 20, 20),
    "highlight_color": (255, 140, 0),
    "box_color": (200, 200, 200),
    "box_highlight": (180, 180, 180),
    "button_color": (100, 100, 240),
    "button_hover_color": (80, 80, 220),
    "button_text_color": (255, 255, 255),
    "padding": 25,
    "text_padding": 14,
    "font_size": 18,
    "title_font_size": 22,
    "small_font_size": 14,
    "animation_speed": 1.0,
    "fps": 60,
    "inactive_color": (180, 180, 180),  # Gray color for inactive buttons
    "button_border_color": (100, 100, 100),  # Border color for buttons
    "subtitle_color": (80, 80, 80),  # Dark gray for subtitles
    "radio_selected_color": (50, 150, 50),  # Green for selected radio button
    "radio_unselected_color": (150, 150, 150),  # Gray for unselected radio button
    "explanation_bg_color": (230, 230, 230),  # Background color for explanation text
    "explanation_text_color": (20, 20, 20),   # Text color for explanation
    "explanation_padding": 5,                 # Padding around explanation text
    "explanation_font_size": 16,              # Font size for explanation text
    "explanation_max_width": 600,             # Maximum width for explanation text
    "explanation_x_offset": 200,               # Horizontal offset from prev button
    "explanation_y_offset": 0,                # Vertical offset from bottom padding
    "explanation_position": "bottom",         # Position: "bottom", "top", or "custom"
    "explanation_custom_x": 500,              # Custom X position (if position is "custom")
    "explanation_custom_y": 700               # Custom Y position (if position is "custom")
}

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((CONFIG["width"], CONFIG["height"]))
pygame.display.set_caption("SHA Visualization")

# Initialize clipboard functionality after display is created
pygame.scrap.init()

# Fonts
pygame.font.init()
try:
    font_path = pygame.font.match_font('arial')
    font = pygame.freetype.Font(font_path, CONFIG["font_size"])
    title_font = pygame.freetype.Font(font_path, CONFIG["title_font_size"])
    small_font = pygame.freetype.Font(font_path, CONFIG["small_font_size"])
except:
    # Fallback to default system font
    font = pygame.freetype.SysFont(None, CONFIG["font_size"])
    title_font = pygame.freetype.SysFont(None, CONFIG["title_font_size"])
    small_font = pygame.freetype.SysFont(None, CONFIG["small_font_size"])

# Create a separate font for explanation text
explanation_font = None  # Will be initialized in main()

# Hash Algorithm Base Class
class HashAlgorithm:
    """Base class for hash algorithms"""
    def __init__(self):
        self.name = "Base"
        self.word_size = 0
        self.block_size = 0
        self.rounds = 0
        self.length_size = 0
        self.padding_offset = 0
        self.k_values = []
        self.init_values = []
        
    def rotr(self, x, n, bits=None):
        """Rotate right: circular right shift"""
        if bits is None:
            bits = self.word_size
        mask = (1 << bits) - 1
        return ((x >> n) | (x << (bits - n))) & mask
    
    def prepare_message_schedule(self, block):
        """Prepare message schedule from block"""
        pass
    
    def compress_block(self, block, hash_values):
        """Compress a single block"""
        pass
    
    def process_message(self, message):
        """Process entire message and return hash"""
        pass
    
    def format_hash(self, hash_values):
        """Format hash values as hex string"""
        pass

# SHA-256 Implementation
class SHA256(HashAlgorithm):
    def __init__(self):
        super().__init__()
        self.name = "SHA-256"
        self.word_size = 32
        self.block_size = 512
        self.rounds = 64
        self.length_size = 64
        self.padding_offset = 448
        
        # SHA-256 constants
        self.k_values = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        
        # Initial hash values
        self.init_values = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
    
    def prepare_message_schedule(self, block):
        # Initialize message schedule array
        w = [0] * self.rounds
        
        # Break block into words
        for i in range(16):
            w[i] = int(block[i*self.word_size:(i+1)*self.word_size], 2)
        
        # Extend the words
        for i in range(16, self.rounds):
            s0 = self.rotr(w[i-15], 7) ^ self.rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = self.rotr(w[i-2], 17) ^ self.rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF
        
        return w
    
    def compress_block(self, block, hash_values):
        # Prepare message schedule
        w = self.prepare_message_schedule(block)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = hash_values
        
        # Compression function main loop
        for i in range(self.rounds):
            S1 = self.rotr(e, 6) ^ self.rotr(e, 11) ^ self.rotr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + self.k_values[i] + w[i]) & 0xFFFFFFFF
            S0 = self.rotr(a, 2) ^ self.rotr(a, 13) ^ self.rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        
        # Update hash values
        new_hash = [
            (hash_values[0] + a) & 0xFFFFFFFF,
            (hash_values[1] + b) & 0xFFFFFFFF,
            (hash_values[2] + c) & 0xFFFFFFFF,
            (hash_values[3] + d) & 0xFFFFFFFF,
            (hash_values[4] + e) & 0xFFFFFFFF,
            (hash_values[5] + f) & 0xFFFFFFFF,
            (hash_values[6] + g) & 0xFFFFFFFF,
            (hash_values[7] + h) & 0xFFFFFFFF
        ]
        
        return new_hash, w, [a, b, c, d, e, f, g, h]
    
    def process_message(self, message):
        # Convert message to binary
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        
        # Pad the message
        message_len = len(binary_message)
        message_len_in_bits = format(message_len, f'0{self.length_size}b')
        
        # Append 1
        padded = binary_message + '1'
        
        # Append 0s until length is congruent to padding_offset mod block_size
        padding_length = (self.padding_offset - len(padded) % self.block_size) % self.block_size
        padded += '0' * padding_length
        
        # Append message length as binary
        padded += message_len_in_bits
        
        # Break the message into blocks
        blocks = [padded[i:i+self.block_size] for i in range(0, len(padded), self.block_size)]
        
        # Initialize hash values
        hash_values = list(self.init_values)
        
        # Process each block
        for block in blocks:
            hash_values, _, _ = self.compress_block(block, hash_values)
        
        # Format final hash
        return self.format_hash(hash_values), binary_message, padded, blocks
    
    def format_hash(self, hash_values):
        return ''.join(format(h, '08x') for h in hash_values)

# SHA-512 Implementation
class SHA512(HashAlgorithm):
    def __init__(self):
        super().__init__()
        self.name = "SHA-512"
        self.word_size = 64
        self.block_size = 1024
        self.rounds = 80
        self.length_size = 128
        self.padding_offset = 896
        
        # SHA-512 constants
        self.k_values = [
            0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
            0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
            0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
            0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
            0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
            0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
            0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
            0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
            0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
            0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
            0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
            0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
            0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
            0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
            0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
            0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
            0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
            0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
            0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
            0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
        ]
        
        # Initial hash values
        self.init_values = [
            0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
            0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
        ]
    
    def prepare_message_schedule(self, block):
        # Initialize message schedule array
        w = [0] * self.rounds
        
        # Break block into words
        for i in range(16):
            w[i] = int(block[i*self.word_size:(i+1)*self.word_size], 2)
        
        # Extend the words
        for i in range(16, self.rounds):
            s0 = self.rotr(w[i-15], 1) ^ self.rotr(w[i-15], 8) ^ (w[i-15] >> 7)
            s1 = self.rotr(w[i-2], 19) ^ self.rotr(w[i-2], 61) ^ (w[i-2] >> 6)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFFFFFFFFFF
        
        return w
    
    def compress_block(self, block, hash_values):
        # Prepare message schedule
        w = self.prepare_message_schedule(block)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = hash_values
        
        # Compression function main loop
        for i in range(self.rounds):
            S1 = self.rotr(e, 14) ^ self.rotr(e, 18) ^ self.rotr(e, 41)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + self.k_values[i] + w[i]) & 0xFFFFFFFFFFFFFFFF
            S0 = self.rotr(a, 28) ^ self.rotr(a, 34) ^ self.rotr(a, 39)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFFFFFFFFFF
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF
        
        # Update hash values
        new_hash = [
            (hash_values[0] + a) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[1] + b) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[2] + c) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[3] + d) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[4] + e) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[5] + f) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[6] + g) & 0xFFFFFFFFFFFFFFFF,
            (hash_values[7] + h) & 0xFFFFFFFFFFFFFFFF
        ]
        
        return new_hash, w, [a, b, c, d, e, f, g, h]
    
    def process_message(self, message):
        # Convert message to binary
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        
        # Pad the message
        message_len = len(binary_message)
        message_len_in_bits = format(message_len, f'0{self.length_size}b')
        
        # Append 1
        padded = binary_message + '1'
        
        # Append 0s until length is congruent to padding_offset mod block_size
        padding_length = (self.padding_offset - len(padded) % self.block_size) % self.block_size
        padded += '0' * padding_length
        
        # Append message length as binary
        padded += message_len_in_bits
        
        # Break the message into blocks
        blocks = [padded[i:i+self.block_size] for i in range(0, len(padded), self.block_size)]
        
        # Initialize hash values
        hash_values = list(self.init_values)
        
        # Process each block
        for block in blocks:
            hash_values, _, _ = self.compress_block(block, hash_values)
        
        # Format final hash
        return self.format_hash(hash_values), binary_message, padded, blocks
    
    def format_hash(self, hash_values):
        return ''.join(format(h, '016x') for h in hash_values)

# Create hash algorithm instances
sha256 = SHA256()
sha512 = SHA512()

# UI Components
class TextBox:
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.freetype.Font, text: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = CONFIG["box_color"]
        self.text = text
        self.font = font
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.text_surface, self.text_rect = self.font.render(self.text, CONFIG["text_color"])
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            return True
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            
            self.text_surface, self.text_rect = self.font.render(self.text, CONFIG["text_color"])
            return True
            
        return False
    
    def update(self, dt: float):
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, surface: pygame.Surface):
        if self.active:
            color = CONFIG["box_highlight"]
        else:
            color = self.color
            
        pygame.draw.rect(surface, color, self.rect, 0)
        pygame.draw.rect(surface, CONFIG["text_color"], self.rect, 2)
        
        # Render text with padding
        text_padding = CONFIG["text_padding"]
        surface.blit(self.text_surface, (self.rect.x + text_padding, self.rect.y + (self.rect.height - self.text_rect.height) // 2))
        
        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_pos = self.rect.x + text_padding + self.text_rect.width
            cursor_height = self.text_rect.height
            pygame.draw.line(
                surface,
                CONFIG["text_color"],
                (cursor_pos, self.rect.y + (self.rect.height - cursor_height) // 2),
                (cursor_pos, self.rect.y + (self.rect.height + cursor_height) // 2),
                2
            )

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.freetype.Font, callback: callable, active: bool = True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
        self.active = active
        self.text_surf, self.text_rect = font.render(text, CONFIG["text_color"])
        
    def draw(self, surface: pygame.Surface):
        # Choose color based on state
        if not self.active:
            color = CONFIG["inactive_color"]
        elif self.hovered:
            color = CONFIG["button_hover_color"]
        else:
            color = CONFIG["button_color"]
            
        # Draw button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, CONFIG["button_border_color"], self.rect, 2, border_radius=5)
        
        # Center text
        text_pos = (
            self.rect.x + (self.rect.width - self.text_rect.width) // 2, 
            self.rect.y + (self.rect.height - self.text_rect.height) // 2
        )
        surface.blit(self.text_surf, text_pos)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.active:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

class RadioButton:
    def __init__(self, x, y, radius, text, font, selected=False, callback=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.font = font
        self.selected = selected
        self.callback = callback
        self.text_surf, self.text_rect = font.render(text, CONFIG["text_color"])
        
    def draw(self, surface):
        # Draw outer circle
        pygame.draw.circle(surface, CONFIG["text_color"], (self.x, self.y), self.radius, 1)
        
        # Draw inner circle if selected
        if self.selected:
            pygame.draw.circle(surface, CONFIG["radio_selected_color"], 
                             (self.x, self.y), self.radius - 3)
        
        # Draw text
        surface.blit(self.text_surf, (self.x + self.radius + 5, 
                                    self.y - self.text_rect.height // 2))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if click is within the circle
            dx = event.pos[0] - self.x
            dy = event.pos[1] - self.y
            if dx*dx + dy*dy <= self.radius*self.radius:
                self.selected = True
                if self.callback:
                    self.callback()
                return True
        return False

class RadioGroup:
    def __init__(self, buttons):
        self.buttons = buttons
        
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                # Deselect all other buttons
                for other in self.buttons:
                    if other != button:
                        other.selected = False
                return True
        return False
        
    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)
            
    def get_selected(self):
        for button in self.buttons:
            if button.selected:
                return button.text
        return None

class Visualization:
    def __init__(self):
        self.current_scene = "intro"
        self.animation_time = 0
        self.message = ""
        self.binary_message = ""
        self.padded_message = ""
        self.blocks = []
        self.current_block_index = 0
        self.schedule = None
        self.hash_values = []
        self.previous_hash_values = []
        self.compression_step = 0
        self.final_hash = ""
        self.step_index = 0
        self.sub_step_index = 0
        self.highlight_index = -1
        self.explanation = ""
        self.current_algorithm = sha256  # Default algorithm
        
        # Text input box
        padding = CONFIG["padding"]
        input_width = CONFIG["width"] - 2 * padding - 100  # Leave space for button
        self.text_box = TextBox(padding, padding, input_width, 40, font)
        
        # Hash button
        button_x = padding + input_width + 10
        self.hash_button = Button(button_x, padding, 90, 40, "Hash", font, self.start_hash)
        
        # Algorithm selection radio buttons - vertical layout under hash button
        radio_x = padding + input_width + 10  # Same x as hash button
        radio_y = padding + 50  # Position below the hash button (40px height + 10px gap)
        self.sha256_radio = RadioButton(radio_x, radio_y, 8, "SHA-256", font, True, 
                                      lambda: self.set_algorithm(sha256))
        self.sha512_radio = RadioButton(radio_x, radio_y + 30, 8, "SHA-512", font, False,  # 30px below SHA-256
                                      lambda: self.set_algorithm(sha512))
        
        self.radio_group = RadioGroup([self.sha256_radio, self.sha512_radio])
        
        # Navigation buttons
        button_width = 100
        button_height = 40
        button_spacing = 10
        
        self.prev_button = Button(
            padding, 
            CONFIG["height"] - padding - button_height, 
            button_width, 
            button_height, 
            "Previous", 
            font, 
            self.previous_step
        )
        
        self.next_button = Button(
            padding + button_width + button_spacing, 
            CONFIG["height"] - padding - button_height, 
            button_width, 
            button_height, 
            "Next", 
            font, 
            self.next_step
        )
        
        self.reset_button = Button(
            CONFIG["width"] - padding - button_width, 
            CONFIG["height"] - padding - button_height, 
            button_width, 
            button_height, 
            "Reset", 
            font, 
            self.reset
        )
        
        # Update scene descriptions
        self.update_scene_descriptions()
    
    def set_algorithm(self, algorithm):
        self.current_algorithm = algorithm
        self.update_scene_descriptions()
    
    def update_scene_descriptions(self):
        self.scenes = {
            "intro": {"title": f"{self.current_algorithm.name} Hash Algorithm", 
                     "description": f"Enter a message to visualize the {self.current_algorithm.name} hashing process."},
            "preprocessing": {"title": "Step 1: Preprocessing", 
                             "description": "Convert the message to binary and pad it."},
            "parsing": {"title": "Step 2: Parsing", 
                       "description": f"Break the padded message into {self.current_algorithm.block_size}-bit blocks."},
            "initialize": {"title": "Step 3: Initialize Hash Values", 
                          "description": "Set up the initial hash values (H0-H7)."},
            "prepare_schedule": {"title": "Step 4: Prepare Message Schedule", 
                                "description": f"Expand the block into {self.current_algorithm.rounds} words."},
            "compression": {"title": "Step 5: Compression Function", 
                           "description": "Process the block through the compression function."},
            "final": {"title": "Final Hash Value", 
                     "description": f"The resulting {self.current_algorithm.name} hash."}
        }
    
    def start_hash(self):
        self.message = self.text_box.text
        if not self.message:
            return
        
        # Process the message
        self.final_hash, self.binary_message, self.padded_message, self.blocks = self.current_algorithm.process_message(self.message)
        
        # Initialize visualization state
        self.current_scene = "preprocessing"
        self.step_index = 0
        self.current_block_index = 0
        self.schedule = None  # Will be initialized when needed
        self.hash_values = list(self.current_algorithm.init_values)
        self.previous_hash_values = list(self.current_algorithm.init_values)
        
        # Pre-calculate schedule for the first block
        if self.blocks:
            current_block = self.blocks[self.current_block_index]
            self.schedule = self.current_algorithm.prepare_message_schedule(current_block)
            print(f"Initialized schedule with {len(self.schedule)} words")
        
        # Update scene descriptions
        self.update_scene_descriptions()
    
    def reset(self):
        self.current_scene = "intro"
        self.step_index = 0
        self.sub_step_index = 0
        self.update_scene_descriptions()
    
    def next_step(self):
        if self.current_scene == "intro":
            if self.message:
                self.current_scene = "preprocessing"
        elif self.current_scene == "preprocessing":
            self.step_index += 1
            if self.step_index > 2:  # After padding steps
                self.step_index = 0
                self.current_scene = "parsing"
        elif self.current_scene == "parsing":
            self.step_index += 1
            if self.step_index > 0:  # After showing blocks
                self.step_index = 0
                self.current_scene = "initialize"
        elif self.current_scene == "initialize":
            self.step_index += 1
            if self.step_index > 7:  # After showing all hash values
                self.step_index = 0
                self.current_scene = "prepare_schedule"
        elif self.current_scene == "prepare_schedule":
            self.step_index += 1
            if self.step_index > 3:  # After showing all schedule words
                self.step_index = 0
                self.current_scene = "compression"
        elif self.current_scene == "compression":
            self.step_index += 1
            if self.step_index >= self.current_algorithm.rounds:  # After all compression rounds
                self.current_scene = "final"
                self.step_index = 0
    
    def previous_step(self):
        if self.current_scene == "preprocessing":
            if self.step_index > 0:
                self.step_index -= 1
            else:
                self.current_scene = "intro"
        elif self.current_scene == "parsing":
            if self.step_index > 0:
                self.step_index -= 1
            else:
                self.current_scene = "preprocessing"
                self.step_index = 2
        elif self.current_scene == "initialize":
            if self.step_index > 0:
                self.step_index -= 1
            else:
                self.current_scene = "parsing"
                self.step_index = 0
        elif self.current_scene == "prepare_schedule":
            if self.step_index > 0:
                self.step_index -= 1
            else:
                self.current_scene = "initialize"
                self.step_index = 7
        elif self.current_scene == "compression":
            if self.step_index > 0:
                self.step_index -= 1
            else:
                self.current_scene = "prepare_schedule"
                self.step_index = 3
        elif self.current_scene == "final":
            self.current_scene = "compression"
            self.step_index = self.current_algorithm.rounds - 1
    
    def update(self, dt: float):
        self.animation_time += dt
        self.text_box.update(dt)
        
        # Handle radio button events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.radio_group.handle_event(event)
    
    def draw(self, surface: pygame.Surface):
        # Clear screen
        surface.fill(CONFIG["bg_color"])
        
        # Draw title and description
        if self.current_scene in self.scenes:
            scene_info = self.scenes[self.current_scene]
            # Include algorithm name in title for all scenes except intro
            if self.current_scene != "intro":
                title = f"{self.current_algorithm.name} - {scene_info['title']}"
            else:
                title = scene_info["title"]
            
            title_surf, title_rect = title_font.render(title, CONFIG["highlight_color"])
            surface.blit(title_surf, (CONFIG["padding"], CONFIG["padding"] * 3))
            
            desc_surf, desc_rect = font.render(scene_info["description"], CONFIG["text_color"])
            surface.blit(desc_surf, (CONFIG["padding"], CONFIG["padding"] * 3 + title_rect.height + 10))
        
        # Draw input box and hash button in intro scene
        if self.current_scene == "intro":
            self.text_box.draw(surface)
            self.hash_button.draw(surface)
            
            # Draw radio buttons
            self.radio_group.draw(surface)
        
        # Draw content based on current scene
        content_rect = pygame.Rect(
            CONFIG["padding"],
            CONFIG["padding"] * 4 + 60,
            CONFIG["width"] - 2 * CONFIG["padding"],
            CONFIG["height"] - CONFIG["padding"] * 6 - 60
        )
        
        if self.current_scene == "preprocessing":
            self.draw_preprocessing(surface, content_rect)
        elif self.current_scene == "parsing":
            self.draw_parsing(surface, content_rect)
        elif self.current_scene == "initialize":
            self.draw_initialize(surface, content_rect)
        elif self.current_scene == "prepare_schedule":
            self.draw_prepare_schedule(surface, content_rect)
        elif self.current_scene == "compression":
            self.draw_compression(surface, content_rect)
        elif self.current_scene == "final":
            self.draw_final(surface, content_rect)
        
        # Draw navigation buttons if not in intro scene
        if self.current_scene != "intro":
            self.prev_button.draw(surface)
            self.next_button.draw(surface)
            self.reset_button.draw(surface)
            
            # Draw explanation text with configurable position
            if hasattr(self, 'current_explanation') and self.current_explanation:
                # Use the dedicated explanation font
                explanation_surf, explanation_rect = explanation_font.render(
                    self.current_explanation, 
                    CONFIG["explanation_text_color"]
                )
                
                # Determine position based on configuration
                if CONFIG["explanation_position"] == "bottom":
                    # Position between prev/next and reset buttons at bottom
                    explanation_x = self.prev_button.rect.right + CONFIG["explanation_x_offset"]
                    explanation_width = self.reset_button.rect.left - explanation_x - CONFIG["explanation_x_offset"]
                    explanation_y = CONFIG["height"] - CONFIG["padding"] - explanation_rect.height + CONFIG["explanation_y_offset"]
                elif CONFIG["explanation_position"] == "top":
                    # Position at top of screen below title
                    explanation_x = CONFIG["padding"]
                    explanation_width = CONFIG["width"] - 2 * CONFIG["padding"]
                    explanation_y = CONFIG["padding"] * 3 + 60 + CONFIG["explanation_y_offset"]
                else:  # "custom"
                    # Use custom position
                    explanation_x = CONFIG["explanation_custom_x"]
                    explanation_width = CONFIG["explanation_max_width"]
                    explanation_y = CONFIG["explanation_custom_y"]
                
                # If text is too wide, wrap it
                if explanation_rect.width > explanation_width:
                    # Split into multiple lines if needed
                    words = self.current_explanation.split()
                    lines = []
                    current_line = []
                    
                    for word in words:
                        test_line = ' '.join(current_line + [word])
                        test_surf, test_rect = explanation_font.render(test_line, CONFIG["explanation_text_color"])
                        
                        if test_rect.width <= explanation_width:
                            current_line.append(word)
                        else:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Draw each line
                    line_height = CONFIG["explanation_font_size"] + 2
                    bg_height = len(lines) * line_height + 2 * CONFIG["explanation_padding"]
                    
                    # Draw background
                    pygame.draw.rect(surface, CONFIG["explanation_bg_color"], 
                                   (explanation_x - CONFIG["explanation_padding"], 
                                    explanation_y - CONFIG["explanation_padding"] - (len(lines) - 1) * line_height, 
                                    min(explanation_width, CONFIG["explanation_max_width"]) + 2 * CONFIG["explanation_padding"], 
                                    bg_height),
                                   border_radius=5)
                    
                    # Draw text lines
                    for i, line in enumerate(lines):
                        line_surf, line_rect = explanation_font.render(line, CONFIG["explanation_text_color"])
                        surface.blit(line_surf, 
                                   (explanation_x, 
                                    explanation_y - (len(lines) - 1 - i) * line_height))
                else:
                    # Draw background
                    pygame.draw.rect(surface, CONFIG["explanation_bg_color"], 
                                   (explanation_x - CONFIG["explanation_padding"], 
                                    explanation_y - CONFIG["explanation_padding"], 
                                    explanation_rect.width + 2 * CONFIG["explanation_padding"], 
                                    explanation_rect.height + 2 * CONFIG["explanation_padding"]),
                                   border_radius=5)
                    
                    # Draw text
                    surface.blit(explanation_surf, (explanation_x, explanation_y))
    
    def draw_preprocessing(self, surface: pygame.Surface, rect: pygame.Rect):
        # Draw original message
        msg_title_surf, msg_title_rect = title_font.render("Original Message:", CONFIG["subtitle_color"])
        surface.blit(msg_title_surf, (rect.x, rect.y))
        
        # If message is too long, truncate with ellipsis
        max_msg_width = rect.width - 40
        msg_surf, msg_rect = font.render(self.message, CONFIG["text_color"])
        if msg_rect.width > max_msg_width:
            truncated = self.message[:30] + "..."
            msg_surf, msg_rect = font.render(truncated, CONFIG["text_color"])
        
        surface.blit(msg_surf, (rect.x, rect.y + msg_title_rect.height + 5))
        
        y_offset = rect.y + msg_title_rect.height + msg_rect.height + 20
        
        # Format binary representation with line breaks
        if self.step_index >= 0:
            bin_title_surf, bin_title_rect = font.render("Binary Representation:", CONFIG["subtitle_color"])
            surface.blit(bin_title_surf, (rect.x, y_offset))
            
            # Format binary into 64-bit chunks with 8-bit spacing
            formatted_lines = []
            binary = self.binary_message
            for i in range(0, len(binary), 64):
                chunk = binary[i:i+64]
                formatted_chunk = ' '.join(chunk[j:j+8] for j in range(0, len(chunk), 8))
                formatted_lines.append(formatted_chunk)
            
            line_height = CONFIG["font_size"] + 5
            for i, line in enumerate(formatted_lines):
                line_surf, line_rect = font.render(line, CONFIG["text_color"])
                surface.blit(line_surf, (rect.x + 20, y_offset + bin_title_rect.height + 5 + i * line_height))
            
            y_offset = y_offset + bin_title_rect.height + (len(formatted_lines) + 1) * line_height
        
        # Draw padding step 1 (append 1)
        if self.step_index >= 1:
            pad1_title_surf, pad1_title_rect = title_font.render("Step 1: Append '1' bit", CONFIG["subtitle_color"])
            surface.blit(pad1_title_surf, (rect.x, y_offset))
            
            # Format binary with spaces between bytes and break into lines if needed
            padded_binary = self.binary_message + "1"
            formatted_lines = []
            for i in range(0, len(padded_binary), 64):
                chunk = padded_binary[i:i+64]
                formatted_chunk = ' '.join(chunk[j:j+8] for j in range(0, len(chunk), 8))
                formatted_lines.append(formatted_chunk)
            
            line_height = CONFIG["font_size"] + 5
            for i, line in enumerate(formatted_lines):
                line_surf, line_rect = font.render(line, CONFIG["text_color"])
                surface.blit(line_surf, (rect.x + 20, y_offset + pad1_title_rect.height + 5 + i * line_height))
            
            y_offset = y_offset + pad1_title_rect.height + (len(formatted_lines) + 1) * line_height
        
        # Draw padding step 2 (append 0s and length)
        if self.step_index >= 2:
            # Determine parameters based on algorithm
            padding_offset = self.current_algorithm.padding_offset
            length_bits_size = self.current_algorithm.length_size
                
            pad2_title_surf, pad2_title_rect = title_font.render("Step 2: Pad with '0's and append original length", CONFIG["subtitle_color"])
            surface.blit(pad2_title_surf, (rect.x, y_offset))
            
            # Add more vertical space after the subtitle
            block_y = y_offset + pad2_title_rect.height + 20  # Increased from 5 to 20
            
            # Format the padded message into smaller chunks with line breaks
            padded = self.binary_message + "1" + "0" * (padding_offset - 1 - len(self.binary_message)) 
            length_bits = format(len(self.binary_message), f'0{length_bits_size}b')
            full_message = padded + length_bits
            
            # For SHA-512, display in two columns of 512 bits each
            if self.current_algorithm.name == "SHA-512" and len(full_message) >= 1024:
                # Configuration for SHA-512 display
                left_column_x = rect.x + 20
                right_column_x = rect.x + 20 + 550  # Increased from 400 to 450 for more space
                row_spacing = 0  # Increased from 5 for more vertical space
                line_height = CONFIG["font_size"] + row_spacing
                
                # First 512 bits in left column
                left_column_bits = full_message[:512]
                
                # Format into 8x8 chunks (8 rows of 8 bytes each)
                for row in range(8):
                    row_start = row * 64
                    row_bits = left_column_bits[row_start:row_start+64]
                    formatted_row = ' '.join(row_bits[j:j+8] for j in range(0, 64, 8))
                    row_surf, row_rect = font.render(formatted_row, CONFIG["text_color"])
                    surface.blit(row_surf, (left_column_x, block_y + row * line_height))
                
                # Second 512 bits in right column
                right_column_bits = full_message[512:1024]
                
                # Format into 8x8 chunks (8 rows of 8 bytes each)
                for row in range(8):
                    row_start = row * 64
                    row_bits = right_column_bits[row_start:row_start+64]
                    formatted_row = ' '.join(row_bits[j:j+8] for j in range(0, 64, 8))
                    row_surf, row_rect = font.render(formatted_row, CONFIG["text_color"])
                    surface.blit(row_surf, (right_column_x, block_y + row * line_height))
                
                # Show padded message length below both columns
                length_y = block_y + 8 * line_height + 10
            else:
                # For SHA-256 or shorter messages, use the original approach
                block_lines = []
                for i in range(0, len(full_message), 64):
                    block = full_message[i:i+64]
                    formatted_block = ' '.join(block[j:j+8] for j in range(0, len(block), 8))
                    block_lines.append(formatted_block)
                
                for i, block in enumerate(block_lines):
                    block_surf, block_rect = font.render(block, CONFIG["text_color"])
                    surface.blit(block_surf, (rect.x + 20, block_y + i * line_height))
                
                length_y = block_y + len(block_lines) * line_height + 10
            
            # Show padded message length
            length_text = f"Final padded length: {len(full_message)} bits"
            length_surf, length_rect = font.render(length_text, CONFIG["text_color"])
            surface.blit(length_surf, (rect.x, length_y))
            
            # Set explanation based on step
            if self.step_index == 0:
                self.current_explanation = f"Converting '{self.message}' to binary representation"
            elif self.step_index == 1:
                self.current_explanation = f"Appending '1' bit to the end of the binary message"
            elif self.step_index == 2:
                if self.current_algorithm.name == "SHA-256":
                    self.current_explanation = "Padding with '0's until message length ≡ 448 (mod 512), then appending 64-bit message length"
                else:  # SHA-512
                    self.current_explanation = "Padding with '0's until message length ≡ 896 (mod 1024), then appending 128-bit message length"
    
    def draw_parsing(self, surface: pygame.Surface, rect: pygame.Rect):
        title_surf, title_rect = title_font.render(f"Parsing into {self.current_algorithm.block_size}-bit Blocks:", CONFIG["subtitle_color"])
        surface.blit(title_surf, (rect.x, rect.y))
        
        y_offset = rect.y + title_rect.height + 10
        
        # Show number of blocks
        num_blocks_text = f"Number of blocks: {len(self.blocks)}"
        num_blocks_surf, num_blocks_rect = font.render(num_blocks_text, CONFIG["text_color"])
        surface.blit(num_blocks_surf, (rect.x, y_offset))
        
        y_offset += num_blocks_rect.height + 20
        
        # Show current block
        if self.blocks:
            block_title = f"Block {self.current_block_index + 1} of {len(self.blocks)}:"
            block_title_surf, block_title_rect = font.render(block_title, CONFIG["subtitle_color"])
            surface.blit(block_title_surf, (rect.x, y_offset))
            
            y_offset += block_title_rect.height + 5
            
            # Format block into 64-bit chunks with 8-bit spacing
            block = self.blocks[self.current_block_index]
            formatted_lines = []
            for i in range(0, len(block), 64):
                chunk = block[i:i+64]
                formatted_chunk = ' '.join(chunk[j:j+8] for j in range(0, len(chunk), 8))
                formatted_lines.append(formatted_chunk)
            
            line_height = CONFIG["font_size"] + 5
            for i, line in enumerate(formatted_lines):
                line_surf, line_rect = font.render(line, CONFIG["text_color"])
                surface.blit(line_surf, (rect.x + 20, y_offset + i * line_height))
        
        # Set explanation
        block_size = "512" if self.current_algorithm.name == "SHA-256" else "1024"
        self.current_explanation = f"Breaking the padded message into {block_size}-bit blocks for processing"
    
    def draw_initialize(self, surface: pygame.Surface, rect: pygame.Rect):
        title_surf, title_rect = title_font.render("Initialize Hash Values:", CONFIG["subtitle_color"])
        surface.blit(title_surf, (rect.x, rect.y))
        
        # Show explanation
        explanation = "The initial hash values are the first 32 bits of the fractional parts of the square roots of the first 8 prime numbers."
        if self.current_algorithm.name == "SHA-512":
            explanation = "The initial hash values are the first 64 bits of the fractional parts of the square roots of the first 8 prime numbers."
        
        explanation_surf, explanation_rect = font.render(explanation, CONFIG["text_color"])
        surface.blit(explanation_surf, (rect.x, rect.y + title_rect.height + 5))
        
        # Show hash values
        y_offset = rect.y + title_rect.height + explanation_rect.height + 20
        for i, value in enumerate(self.current_algorithm.init_values):
            # Format based on algorithm
            format_width = 16 if self.current_algorithm.name == "SHA-512" else 8
            text = f"H{i} = {format(value, f'0{format_width}x')}"
            value_surf, value_rect = font.render(text, CONFIG["text_color"])
            
            # Highlight current value
            if i == self.step_index:
                pygame.draw.rect(surface, CONFIG["highlight_color"], 
                               (rect.x + 15, y_offset - 2, value_rect.width + 10, value_rect.height + 4))
            
            surface.blit(value_surf, (rect.x + 20, y_offset))
            y_offset += value_rect.height + 5
        
        # Set explanation based on step
        if self.step_index <= 7:
            self.current_explanation = f"Initializing hash value H{self.step_index} with a constant derived from prime numbers"
    
    def draw_prepare_schedule(self, surface: pygame.Surface, rect: pygame.Rect):
        title_surf, title_rect = title_font.render("Message Schedule Words:", CONFIG["highlight_color"])
        surface.blit(title_surf, (rect.x, rect.y))
        
        # Add explanation based on step and algorithm
        if self.current_algorithm.name == "SHA-256":
            if self.step_index == 0:
                self.current_explanation = "First 16 words (W0-W15) are taken directly from the 512-bit message block"
                end_idx = 16
            elif self.step_index == 1:
                self.current_explanation = "Words W16-W31 are calculated using: W[i] = W[i-16] + s0 + W[i-7] + s1, where s0 and s1 are rotation functions"
                end_idx = 32
            elif self.step_index == 2:
                self.current_explanation = "Words W32-W47 continue the expansion pattern using the same formula"
                end_idx = 48
            else:
                self.current_explanation = "Words W48-W63 complete the message schedule using the same formula"
                end_idx = 64
        else:  # SHA-512
            if self.step_index == 0:
                self.current_explanation = "First 16 words (W0-W15) are taken directly from the 1024-bit message block"
                end_idx = 16
            elif self.step_index == 1:
                self.current_explanation = "Words W16-W31 are calculated using: W[i] = W[i-16] + s0 + W[i-7] + s1, where s0 and s1 are rotation functions"
                end_idx = 32
            elif self.step_index == 2:
                self.current_explanation = "Words W32-W63 continue the expansion pattern using the same formula"
                end_idx = 64
            else:
                self.current_explanation = "Words W64-W79 complete the message schedule using the same formula"
                end_idx = 80
        
        explanation_surf, explanation_rect = font.render(self.current_explanation, CONFIG["text_color"])
        surface.blit(explanation_surf, (rect.x, rect.y + title_rect.height + 5))
        
        y_offset = rect.y + title_rect.height + explanation_rect.height + 15
        words_per_line = 4  # Always show 4 words per line
        
        # Use same spacing for both algorithms to prevent overlap
        word_width = 200  # Increased width for both SHA-256 and SHA-512
        
        # Check if schedule exists and has enough elements
        if not hasattr(self, 'schedule') or not self.schedule:
            # Prepare the schedule if it doesn't exist
            if self.blocks:
                current_block = self.blocks[self.current_block_index]
                self.schedule = self.current_algorithm.prepare_message_schedule(current_block)
        
        # Debug output
        if self.schedule:
            print(f"Schedule length: {len(self.schedule)}, end_idx: {end_idx}")
        
        # Draw all words up to current step, but only if they exist in the schedule
        if self.schedule:
            for i in range(0, min(end_idx, len(self.schedule))):
                x = rect.x + (i % words_per_line) * word_width
                y = y_offset + (i // words_per_line) * (CONFIG["font_size"] + 10)  # Add more vertical spacing
                
                # Format based on algorithm
                format_width = 16 if self.current_algorithm.name == "SHA-512" else 8
                text = f"W{i:2d} = {format(self.schedule[i], f'0{format_width}x')}"
                word_surf, word_rect = font.render(text, CONFIG["text_color"])
                
                # Highlight new words for current step
                if (self.current_algorithm.name == "SHA-256" and 
                    ((16 <= i < 32 and self.step_index == 1) or 
                     (32 <= i < 48 and self.step_index == 2) or 
                     (48 <= i < 64 and self.step_index == 3))) or \
                   (self.current_algorithm.name == "SHA-512" and 
                    ((16 <= i < 32 and self.step_index == 1) or 
                     (32 <= i < 64 and self.step_index == 2) or 
                     (64 <= i < 80 and self.step_index == 3))):
                    pygame.draw.rect(surface, CONFIG["highlight_color"], 
                                   (x - 2, y - 2, word_rect.width + 4, word_rect.height + 4))
                
                surface.blit(word_surf, (x, y))
    
    def draw_compression(self, surface: pygame.Surface, rect: pygame.Rect):
        title_surf, title_rect = title_font.render(f"Compression Function (Round {self.step_index + 1}/{self.current_algorithm.rounds}):", CONFIG["subtitle_color"])
        surface.blit(title_surf, (rect.x, rect.y))
        
        # Add skip to end button
        self.skip_to_end_btn = Button(
            rect.x + title_rect.width + 20,
            rect.y,
            120, 25, "Skip to End", small_font,
            self.skip_to_end
        )
        self.skip_to_end_btn.draw(surface)
        
        # Use pre-calculated states instead of recalculating
        if hasattr(self, 'compression_states') and len(self.compression_states) > self.step_index:
            a, b, c, d, e, f, g, h = self.compression_states[self.step_index]
            self.hash_values = [a, b, c, d, e, f, g, h]
        
        # Draw working variables
        y_offset = rect.y + title_rect.height + 10
        variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        format_width = 16 if self.current_algorithm.name == "SHA-512" else 8
        
        for i, var in enumerate(variables):
            value = self.hash_values[i]
            text = f"{var} = {format(value, f'0{format_width}x')}"
            var_surf, var_rect = font.render(text, CONFIG["text_color"])
            surface.blit(var_surf, (rect.x + 20, y_offset))
            y_offset += var_rect.height + 5
        
        # Draw current round details
        round_y = y_offset + 20
        round_text = f"Round {self.step_index + 1}: Using message schedule word W{self.step_index} = {format(self.schedule[self.step_index], f'0{format_width}x')}"
        round_surf, round_rect = font.render(round_text, CONFIG["subtitle_color"])
        surface.blit(round_surf, (rect.x, round_y))
        
        # Draw K constant
        k_y = round_y + round_rect.height + 5
        k_text = f"K{self.step_index} = {format(self.current_algorithm.k_values[self.step_index], f'0{format_width}x')}"
        k_surf, k_rect = font.render(k_text, CONFIG["text_color"])
        surface.blit(k_surf, (rect.x + 20, k_y))
        
        # Set explanation based on step
        round_text = f"Round {self.step_index + 1}/{self.current_algorithm.rounds}"
        if self.current_algorithm.name == "SHA-256":
            self.current_explanation = f"{round_text}: Applying compression function to update working variables a-h using message schedule word W{self.step_index}"
        else:  # SHA-512
            self.current_explanation = f"{round_text}: Applying compression function to update working variables a-h using message schedule word W{self.step_index}"
    
    def draw_final(self, surface: pygame.Surface, rect: pygame.Rect):
        # Show algorithm used
        algo_title_surf, algo_title_rect = title_font.render(f"Algorithm: {self.current_algorithm.name}", CONFIG["highlight_color"])
        surface.blit(algo_title_surf, (rect.x, rect.y))
        
        # Show input message with copy button
        msg_y = rect.y + algo_title_rect.height + 20
        msg_title_surf, msg_title_rect = font.render("Input Message:", CONFIG["subtitle_color"])
        surface.blit(msg_title_surf, (rect.x, msg_y))
        
        msg_surf, msg_rect = font.render(self.message, CONFIG["text_color"])
        surface.blit(msg_surf, (rect.x + 20, msg_y + msg_title_rect.height + 5))
        
        # Add copy buttons
        self.copy_msg_btn = Button(
            rect.x + msg_rect.width + 40, 
            msg_y + msg_title_rect.height + 5,
            80, 25, "Copy", small_font,
            self.copy_message
        )
        self.copy_msg_btn.draw(surface)
        
        # Show final hash with copy button
        hash_y = msg_y + msg_title_rect.height + msg_rect.height + 30
        hash_title_surf, hash_title_rect = font.render(f"Final {self.current_algorithm.name} Hash:", CONFIG["subtitle_color"])
        surface.blit(hash_title_surf, (rect.x, hash_y))
        
        hash_surf, hash_rect = font.render(self.final_hash, CONFIG["text_color"])
        surface.blit(hash_surf, (rect.x + 20, hash_y + hash_title_rect.height + 5))
        
        self.copy_hash_btn = Button(
            rect.x + hash_rect.width + 40,
            hash_y + hash_title_rect.height + 5,
            80, 25, "Copy", small_font,
            self.copy_hash
        )
        self.copy_hash_btn.draw(surface)
        
        # Set explanation
        self.current_explanation = f"Final {self.current_algorithm.name} hash value: {self.final_hash}"
    
    def copy_message(self):
        pygame.scrap.put(pygame.SCRAP_TEXT, self.message.encode())
    
    def copy_hash(self):
        pygame.scrap.put(pygame.SCRAP_TEXT, self.final_hash.encode())

    def skip_to_end(self):
        if self.current_scene == "compression":
            # Make sure schedule is properly initialized
            if not hasattr(self, 'schedule') or not self.schedule or len(self.schedule) < self.current_algorithm.rounds:
                # Re-prepare the schedule if needed
                if self.blocks:
                    current_block = self.blocks[self.current_block_index]
                    self.schedule = self.current_algorithm.prepare_message_schedule(current_block)
            
            # Only proceed if we have a valid schedule
            if self.schedule and len(self.schedule) >= self.current_algorithm.rounds:
                self.step_index = self.current_algorithm.rounds - 1
                # Recalculate final hash values
                self.hash_values = list(self.current_algorithm.init_values)
                
                # Perform all compression rounds at once
                for i in range(self.current_algorithm.rounds):
                    # Perform compression calculation
                    if self.current_algorithm.name == "SHA-256":
                        a, b, c, d, e, f, g, h = self.hash_values
                        
                        # SHA-256 compression function
                        S1 = self.current_algorithm.rotr(e, 6) ^ self.current_algorithm.rotr(e, 11) ^ self.current_algorithm.rotr(e, 25)
                        ch = (e & f) ^ ((~e) & g)
                        temp1 = (h + S1 + ch + self.current_algorithm.k_values[i] + self.schedule[i]) & 0xFFFFFFFF
                        S0 = self.current_algorithm.rotr(a, 2) ^ self.current_algorithm.rotr(a, 13) ^ self.current_algorithm.rotr(a, 22)
                        maj = (a & b) ^ (a & c) ^ (b & c)
                        temp2 = (S0 + maj) & 0xFFFFFFFF
                        
                        h = g
                        g = f
                        f = e
                        e = (d + temp1) & 0xFFFFFFFF
                        d = c
                        c = b
                        b = a
                        a = (temp1 + temp2) & 0xFFFFFFFF
                        
                        self.hash_values = [a, b, c, d, e, f, g, h]
                    else:  # SHA-512
                        a, b, c, d, e, f, g, h = self.hash_values
                        
                        # SHA-512 compression function
                        S1 = self.current_algorithm.rotr(e, 14, 64) ^ self.current_algorithm.rotr(e, 18, 64) ^ self.current_algorithm.rotr(e, 41, 64)
                        ch = (e & f) ^ ((~e) & g)
                        temp1 = (h + S1 + ch + self.current_algorithm.k_values[i] + self.schedule[i]) & 0xFFFFFFFFFFFFFFFF
                        S0 = self.current_algorithm.rotr(a, 28, 64) ^ self.current_algorithm.rotr(a, 34, 64) ^ self.current_algorithm.rotr(a, 39, 64)
                        maj = (a & b) ^ (a & c) ^ (b & c)
                        temp2 = (S0 + maj) & 0xFFFFFFFFFFFFFFFF
                        
                        h = g
                        g = f
                        f = e
                        e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
                        d = c
                        c = b
                        b = a
                        a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF
                        
                        self.hash_values = [a, b, c, d, e, f, g, h]
                
                # Update final hash
                for i in range(8):
                    mask = 0xFFFFFFFFFFFFFFFF if self.current_algorithm.name == "SHA-512" else 0xFFFFFFFF
                    self.hash_values[i] = (self.previous_hash_values[i] + self.hash_values[i]) & mask
                
                format_width = 16 if self.current_algorithm.name == "SHA-512" else 8
                self.final_hash = ''.join(format(h, f'0{format_width}x') for h in self.hash_values)

# Main game loop
def main():
    global explanation_font
    
    # Initialize pygame
    pygame.init()
    pygame.freetype.init()
    pygame.scrap.init()
    
    # Initialize fonts
    global font, title_font, small_font
    font = pygame.freetype.SysFont("Arial", CONFIG["font_size"])
    title_font = pygame.freetype.SysFont("Arial", CONFIG["title_font_size"])
    small_font = pygame.freetype.SysFont("Arial", CONFIG["small_font_size"])
    explanation_font = pygame.freetype.SysFont("Arial", CONFIG["explanation_font_size"])
    
    clock = pygame.time.Clock()
    visualization = Visualization()
    
    while True:
        dt = clock.tick(CONFIG["fps"]) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            visualization.text_box.handle_event(event)
            visualization.hash_button.handle_event(event)
            visualization.radio_group.handle_event(event)
            visualization.prev_button.handle_event(event)
            visualization.next_button.handle_event(event)
            visualization.reset_button.handle_event(event)
            
            # Handle copy buttons if in final scene
            if visualization.current_scene == "final":
                if hasattr(visualization, 'copy_msg_btn'):
                    visualization.copy_msg_btn.handle_event(event)
                if hasattr(visualization, 'copy_hash_btn'):
                    visualization.copy_hash_btn.handle_event(event)
            
            # Handle skip to end button if in compression scene
            if visualization.current_scene == "compression":
                if hasattr(visualization, 'skip_to_end_btn'):
                    visualization.skip_to_end_btn.handle_event(event)
        
        visualization.update(dt)
        visualization.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()