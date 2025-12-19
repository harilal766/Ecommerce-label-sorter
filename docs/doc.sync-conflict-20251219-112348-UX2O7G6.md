pdf_label_sorter/
│
├── pdf_label_sorter/           # Main package directory
│   ├── __init__.py
│   ├── core.py                 # Core sorting logic
│   ├── pdf_utils.py            # Common PDF processing utilities
│   ├── platforms/              # Platform-specific processing modules
│   │   ├── __init__.py
│   │   ├── amazon.py
│   │   └── shopify.py
│   │   └── ...                 # Future platforms go here
│   └── exceptions.py           # Custom exception definitions
│
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_amazon.py
│   └── test_shopify.py
│
├── docs/                       # Documentation (optional but recommended)
│   └── ...
│
├── setup.py                    # Packaging script
├── requirements.txt            # List of dependencies
├── README.md                   # Project overview and usage
├── LICENSE                     # License file
└── .gitignore
