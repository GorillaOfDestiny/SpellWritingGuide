import json
import requests

class SpellLookupService:
    @staticmethod
    def lookup(spell_name):
        try:
            with open('spells.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("spells.json file not found.")
            return

        spell_name = spell_name.lower()

        spells = data.get('results', [])

        for spell in spells:
            if spell.get('name', '').lower() == spell_name:
                print(f"\nSpell Found!\n")
                print(f"Name: {spell.get('name', 'Unknown')}")
                print(f"Index: {spell.get('index', 'Unknown')}")
                print(f"URL: {spell.get('url', 'Unknown')}")
                
                full_url = f"https://www.dnd5eapi.co{spell.get('url')}"
                try:
                    response = requests.get(full_url)
                    if response.status_code == 200:
                        full_spell_data = response.json()
                        print(f"\n--- Full Spell Details ---")
                        print(f"Description: {full_spell_data.get('desc', ['No description'])[0]}")
                        print(f"Level: {full_spell_data.get('level', 'Unknown')}")
                        print(f"Casting Time: {full_spell_data.get('casting_time', 'Unknown')}")
                        print(f"Duration: {full_spell_data.get('duration', 'Unknown')}")
                        print(f"Range: {full_spell_data.get('range', 'Unknown')}")
                    else:
                        print("Failed to fetch full spell details (API error).")
                except requests.RequestException:
                    print("Network error while trying to fetch full spell details.")
                
                return

        print("Spell not found.\n")
