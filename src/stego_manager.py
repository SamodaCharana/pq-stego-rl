"""
stego_manager.py
Coordinates fragment allocation using RL agent
and delegates embedding/extraction to stego_image and stego_audio.
"""

from typing import List, Dict
from rl_agent import RLAgent
from fragmenter import split_ciphertext, reassemble_fragments

# Import your low-level stego modules
import stego_image
import stego_audio


class StegoManager:
    def __init__(self, rl_agent: RLAgent):
        self.agent = rl_agent

    def embed_fragments(self, ciphertext: bytes, num_fragments: int, image_path: str, audio_path: str) -> Dict:
        """
        Embed ciphertext fragments into image/audio carriers.

        Args:
            ciphertext (bytes): The ciphertext to embed.
            num_fragments (int): How many fragments to create.
            image_path (str): Path to cover image.
            audio_path (str): Path to cover audio.

        Returns:
            Dict: Mapping of carriers to stego outputs.
        """
        fragments = split_ciphertext(ciphertext, num_fragments)
        carrier_map = {"image": [], "audio": []}

        for i, frag in enumerate(fragments):
            action = self.agent.choose_action(len(frag))

            if action == "image":
                stego_img = stego_image.embed_image_lsb(image_path, f"stego_image_{i}.png", frag)
                carrier_map["image"].append((stego_img, len(frag)))
            else:
                stego_aud = stego_audio.embed_audio_lsb(audio_path, f"stego_audio_{i}.wav", frag)
                carrier_map["audio"].append((stego_aud, len(frag)))

            # Example reward: fragment closer to "fit" size gives better reward
            reward = -abs(len(frag) - (50 if action == "image" else 70))
            next_frag_size = len(fragments[i + 1]) if i < len(fragments) - 1 else 0
            self.agent.update_q(len(frag), action, reward, next_frag_size)

        return carrier_map

    def extract_fragments(self, carrier_map: Dict) -> bytes:
        """
        Extract ciphertext fragments and reassemble.

        Args:
            carrier_map (Dict): Mapping of stego carriers to (file, payload_len).

        Returns:
            bytes: Reassembled ciphertext.
        """
        fragments = []

        for img, size in carrier_map.get("image", []):
            fragments.append(stego_image.extract_image_lsb(img, size))

        for aud, size in carrier_map.get("audio", []):
            fragments.append(stego_audio.extract_audio_lsb(aud, size))

        return reassemble_fragments(fragments)


# ============
# Simple Test
# ============
if __name__ == "__main__":
    agent = RLAgent()
    manager = StegoManager(agent)

    # Fake ciphertext (160 bytes)
    fake_ct = b"0123456789ABCDEF" * 10

    result = manager.embed_fragments(fake_ct, num_fragments=5, image_path="cover.png", audio_path="cover.wav")
    print("Embedding complete. Carriers used:", {k: len(v) for k, v in result.items()})

    recovered = manager.extract_fragments(result)
    print("Recovery OK:", recovered == fake_ct)
