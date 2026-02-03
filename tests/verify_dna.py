from ray_studio.dna import load_dna
from pathlib import Path

def test_load_dna():
    dna_path = Path("examples/client_dna_example.yaml")
    dna = load_dna(dna_path)

    print(f"Successfully loaded DNA for: {dna.brand.name}")
    assert dna.brand.name == "Acme Corp"
    assert dna.brand.colors.primary == "#1E40AF"
    assert len(dna.products) == 1
    assert dna.products[0].name == "Pro Plan"
    print("All assertions passed!")

if __name__ == "__main__":
    test_load_dna()
