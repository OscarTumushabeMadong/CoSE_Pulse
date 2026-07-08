from repository import Repository

repository = Repository()


def show(label, rows):
    print()
    print("=" * 60)
    print(label)
    print("=" * 60)
    print(f"Count: {len(rows)}")

    for row in rows[:5]:
        print(f"- [{row.get('priority')}] {row.get('title') or row.get('url')}")


def main():
    show("New Pages", repository.get_new_pages())
    show("Updated Pages", repository.get_updated_pages())
    show("Events", repository.get_events())
    show("Scholarships", repository.get_scholarships())
    show("Internships", repository.get_internships())
    show("High Priority Pages", repository.get_high_priority_pages())


if __name__ == "__main__":
    main()
