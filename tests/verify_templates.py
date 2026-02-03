from ray_studio.templates import list_templates, get_template

def test_templates():
    templates = list_templates()
    print(f"Found {len(templates)} templates.")

    expected_templates = ["promo", "testimonial", "product_showcase"]
    found_names = [t.name for t in templates]

    for name in expected_templates:
        assert name in found_names
        print(f"Verified template: {name}")

        # Load individually
        tmpl = get_template(name)
        assert tmpl.name == name
        assert tmpl.inputs is not None

    print("All template tests passed!")

if __name__ == "__main__":
    test_templates()
