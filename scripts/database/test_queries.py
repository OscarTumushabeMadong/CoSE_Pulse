from repository import (
    get_events,
    get_high_priority_pages,
    get_internships,
    get_new_pages,
    get_scholarships,
    get_updated_pages,
)


def show(label, rows):
    print()
    print("=" * 60)
    print(label)
    print("=" * 60)
    print(f"Count: {len(rows)}")

    for row in rows[:5]:
        print(f"- [{row.get('priority')}] {row.get('title') or row.get('url')}")


def main():
    show("New Pages", get_new_pages())
    show("Updated Pages", get_updated_pages())
    show("Events", get_events())
    show("Scholarships", get_scholarships())
    show("Internships", get_internships())
    show("High Priority Pages", get_high_priority_pages())


if __name__ == "__main__":
    main()