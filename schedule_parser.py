import pandas as pd

EXCEL_PATH = r"C:\Users\david\OneDrive\Desktop\M603 Advanced Algorithms\trabajo\Tentative Schedule Data.xlsx"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def load_freelancers(path):
    # Load external/contracted teachers and their availability
    df = pd.read_excel(path, sheet_name="Freelancers Availability")
    df.columns = ["Name", "Availability"]
    df = df.dropna(subset=["Name"])
    df["Name"] = df["Name"].str.strip()
    df["Availability"] = df["Availability"].fillna("").str.strip()
    df["Type"] = "Freelancer"
    return df


def load_internal_faculty(path):
    # Load full-time staff (base professors)
    df = pd.read_excel(path, sheet_name="Internal Faculty")
    df.columns = ["Name", "Notes"]
    df = df.dropna(subset=["Name"])
    df["Name"] = df["Name"].str.strip()
    df["Notes"] = df["Notes"].fillna("").str.strip()
    df["Type"] = "Internal Faculty"
    return df


def load_potsdam_rooms(path):
    # Load Potsdam rooms — only "Gisma" slots are available, "UE" belongs to the other university
    df = pd.read_excel(path, sheet_name="Rooms in Potsdam", header=1)
    df = df.dropna(subset=["Room"])
    df["Room"] = df["Room"].astype(str).str.strip()
    df["Capacity"] = pd.to_numeric(df["Capacity"], errors="coerce")

    records = []
    for _, row in df.iterrows():
        for day in DAYS:
            if day not in row.index:
                continue
            cell = str(row[day]).strip() if pd.notna(row[day]) else ""
            available = cell.lower().startswith("gisma")  # ignore "UE" cells
            records.append({
                "Room": row["Room"],
                "Capacity": int(row["Capacity"]) if pd.notna(row["Capacity"]) else None,
                "Day": day,
                "Available": available,
                "Note": cell if available else ""
            })
    return pd.DataFrame(records)


def potsdam_matrix(rooms_df):
    # Pivot table: rooms as rows, days as columns
    return rooms_df.pivot(index="Room", columns="Day", values="Available")[DAYS]


def all_teachers(freelancers, faculty):
    # Merge both teacher types into a single DataFrame
    faculty = faculty.rename(columns={"Notes": "Availability"})
    return pd.concat(
        [freelancers[["Name", "Availability", "Type"]],
         faculty[["Name", "Availability", "Type"]]],
        ignore_index=True
    )


if __name__ == "__main__":
    # Load all data (Berlin rooms sheet is intentionally ignored)
    freelancers = load_freelancers(EXCEL_PATH)
    faculty     = load_internal_faculty(EXCEL_PATH)
    potsdam     = load_potsdam_rooms(EXCEL_PATH)
    teachers    = all_teachers(freelancers, faculty)
    matrix      = potsdam_matrix(potsdam)

    print(f"\n FREELANCERS ({len(freelancers)}) ")
    for _, r in freelancers.iterrows():
        print(f"  {r['Name']:20s} | {r['Availability'] or '(no details)'}")

    print(f"\n INTERNAL FACULTY ({len(faculty)}) ")
    for _, r in faculty.iterrows():
        print(f"  {r['Name']:20s} | {r['Notes'] or '(no notes)'}")

    print("\n POTSDAM ROOMS (Gisma only) ")
    print(matrix.replace({True: "✓", False: "✗"}).to_string())

    print("\n AVAILABLE ROOMS PER DAY")
    counts = potsdam[potsdam["Available"]].groupby("Day")["Room"].count().reindex(DAYS, fill_value=0)
    for day, n in counts.items():
        print(f"  {day:<12}: {n} room(s)")

    # Export results to CSV in the current folder
    teachers.to_csv("teachers_all.csv", index=False)
    potsdam.to_csv("potsdam_rooms.csv", index=False)
    matrix.to_csv("potsdam_availability_matrix.csv")
    print("\nCSV files saved in current folder.")