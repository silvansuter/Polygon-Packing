# Optimal 2D Packing of Convex Polygons

## Introduction

Optimal packing of objects in containers is a fundamental problem with extensive real-life and industrial applications. The act of efficiently packing a collection of objects into a designated container manifests in various everyday scenarios, such as fitting items on a shelf or arranging cookies on a baking tray.

This project specifically dives into two-dimensional packing problems, which are paramount in many industries. Whether it's cutting shapes from rolled-out dough, manufacturing tile sets from standard-sized wooden, glass, or metal panels, or tailoring fabric pieces for clothing that need to maintain a specific pattern, the challenges of 2D packing are ubiquitous.

The vast applicability of 2D packing has driven significant interest in the development of efficient algorithms. This repository presents and demonstrates a part of the algorithms from the research paper titled "[Improved Approximation Algorithms for Translational Packing of Polygons](https://drops-beta.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2023.76)," co-authored by Adam Kurpisz and me, presented at the European Symposium on Algorithms (ESA) in 2023. These results were the culmination of my Master's thesis research at ETH Zurich.

## Problem Statement

While axis-parallel rectangle packing has numerous open challenges, our focus is on packing convex polygons without rotations in various settings. The aim is to design algorithms that are both fast and accurate, given the inherent complexity of such packing problems.

## Highlights

- The introduced algorithm offers an approximation guarantee of 9.44..., marking a notable improvement from previous algorithms.
- This work builds upon the foundation of existing algorithms, with a particular emphasis on enhancing the approximation guarantee, which stands as a testament to the algorithm's efficiency.
- (TODO: Add a section about the previously best-known approximation algorithm's guarantee once available.)

## Visual Demonstrations

(Embed images/GIFs of your visualizations here.)

## Installation and Usage

### Prerequisites

Before you can run the code, ensure you have the following prerequisites set up:

- **Python:** You should have Python (version 3.x) installed. If not, [download and install](https://www.python.org/downloads/) it.
- **Virtual Environment** (optional but recommended): Using a virtual environment ensures that the dependencies for this project won't interfere with other projects you might have. You can set one up using `venv`:

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

### Setup

Follow the steps below to obtain the code and set it up:

1. **Clone the Repository:**
   
```bash
git clone https://github.com/your_username/your_project_name.git
cd your_project_name
```

2. **Install Dependencies:**
   
If you have a `requirements.txt` or `Pipfile`:

```bash
pip install -r requirements.txt
```

### Running the Code

Here's how you can run the application:

- **Running the Algorithm:**

Use the command or script to execute the primary function of your application:

```bash
python main.py  # Replace with your main script if it's named differently.
```

Make sure to include any arguments or options users can provide and offer a brief explanation of their purpose.

## Code Examples

(Showcase snippets of your algorithm or other interesting parts of your code.)

## Performance Metrics

(Detail the efficiency of your algorithms, their limitations, and areas of potential enhancement.)

## Licensing

This project is licensed under the MIT License. This allows others to use, modify, and distribute this software without restriction.

For full details, please see the [LICENSE](./LICENSE) file in the repository.

## Acknowledgments

Special thanks to Adam Kurpisz for co-authoring the research paper and to ETH Zurich for providing the platform for this research.
