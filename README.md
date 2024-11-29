# Systems Engineering Emerging Topics Analysis

## Project Overview
This project analyzes research articles to identify emerging topics in Systems Engineering using the Systems Engineering Concept Model (SECM) and SEBoK framework.

## Project Structure
```
├── README.md
├── main.py
├── data
│   ├── SECM
│   ├── concept_list_names.txt
│   ├── data.json
│   ├── diagram_list_names.txt
│   └── parseXML.py
├── diagrams
│   ├── drawHeatmap.py
│   └── outputDiagram.jpg
└── tests
    ├── test_diagram_1.xml
    └── test_get_shapes.py
```

## Key Features
- Process large numbers of research articles
- Map research concepts to Systems Engineering Concept Model (SECM)
- Visualize emphasis across SEBoK knowledge areas
- Generate heatmap diagrams of research trends

## Dependencies
- Python 3.8+
- XML parsing libraries
- Data visualization tools

## Installation
```bash
git clone https://github.com/your-username/systems-engineering-research-analysis.git
cd systems-engineering-research-analysis
pip install -r requirements.txt
```

## Usage
```bash
python main.py --input research_articles.xml
```

## Research Methodology
1. Extract research article metadata
2. Map concepts to SECM
3. Analyze distribution across SEBoK areas
4. Generate visual representations

## Contributing
- Open issues for bug reports or feature requests
- Submit pull requests with improvements

## Acknowledgements 
[OMG - Systems Engineering Concept Model (SECM) Working Group](https://www.omgwiki.org/OMGSysML/doku.php?id=sysml-roadmap:systems_engineering_concept_model_workgroup)

[SEBoK - Part 8: Emerging Knowledge](https://sebokwiki.org/wiki/Emerging_Knowledge)

