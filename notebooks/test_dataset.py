import sys
from pathlib import Path
import pandas as pd

# Set up paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.model_utils import load_dataset, clean_text

print("=" * 60)
print("DATASET QUALITY TEST")
print("=" * 60)

# Load dataset
dataset_path = project_root / "data/raw/messages_dataset.csv"
print(f"\n✓ Loading dataset from: {dataset_path}")

df = load_dataset(str(dataset_path))
print(f"✓ Dataset loaded successfully!")

# Basic info
print(f"\n--- Dataset Information ---")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Show sample
print(f"\n--- First 5 rows ---")
print(df.head())

# Class distribution
print(f"\n--- Class Distribution ---")
print(df["label"].value_counts())

# Quality checks
print(f"\n--- Quality Validation ---")

# Check 1: Missing values
print(f"✓ Missing values: {df.isnull().sum().sum()}")

# Check 2: Empty texts
empty_text = df[df["text"].astype(str).str.strip() == ""]
print(f"✓ Empty text messages: {len(empty_text)}")

# Check 3: Empty cleaned text
empty_cleaned = df[df["clean_text"].astype(str).str.strip() == ""]
print(f"✓ Empty cleaned text: {len(empty_cleaned)}")

# Check 4: Valid labels only
print(f"✓ Unique labels: {sorted(df['label'].unique())}")
invalid_labels = df[~df['label'].isin(['safe', 'phishing'])]
print(f"✓ Invalid labels count: {len(invalid_labels)}")

# Check 5: Class balance
safe_count = len(df[df['label'] == 'safe'])
phishing_count = len(df[df['label'] == 'phishing'])
print(f"\n✓ Safe messages: {safe_count}")
print(f"✓ Phishing messages: {phishing_count}")

balance_ratio = min(safe_count, phishing_count) / max(safe_count, phishing_count)
print(f"✓ Balance ratio: {balance_ratio:.2%}")

# Check 6: Language distribution
print(f"\n--- Language Distribution ---")
print(df["language"].value_counts())

# Check 7: Tunisian context
print(f"\n--- Tunisian Context Distribution ---")
tunisian = df[df['is_tunisian_context'] == 1]
print(f"Total Tunisian context messages: {len(tunisian)}")
print(f"Phishing with Tunisian context: {len(tunisian[tunisian['label'] == 'phishing'])}")

# Final summary
print(f"\n" + "=" * 60)
print("VALIDATION CHECKLIST")
print("=" * 60)

checks = {
    "✓ CSV loads correctly": len(df) > 0,
    "✓ No missing values": df.isnull().sum().sum() == 0,
    "✓ No empty texts": len(empty_text) == 0,
    "✓ Only safe/phishing labels": len(invalid_labels) == 0,
    "✓ Text is cleanable": len(empty_cleaned) <= 15,  # Allow few empty cleanings for short msgs
    "✓ Classes balanced": balance_ratio >= 0.55,  # 55% acceptable for hackathon (60/40 split)
    "✓ Minimum size (100+)": len(df) >= 100,
    "✓ clean_text column exists": "clean_text" in df.columns,
    "✓ Tunisian examples (20+)": len(tunisian) >= 20,
}

all_passed = True
for check, status in checks.items():
    symbol = "✓" if status else "✗"
    print(f"{symbol} {check}")
    if not status:
        all_passed = False

print()
if all_passed:
    print("🎉 ALL CHECKS PASSED! Dataset is ready for training!")
else:
    print("⚠ Some checks failed - review dataset")
