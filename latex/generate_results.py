#!/usr/bin/env python3

# Extract values from the huffman_code.py output and generate LaTeX commands

results = """
Block length k = 1 (optimal code)
Alphabet size |Σᵏ|      :   6
Entropy H(Sᵏ)          : 2.4058 bits
Expected length E[L]   : 2.4500 bits
Average length  L̄     : 2.4450 bits
Compression ratio log₂|Σᵏ| / L̄ : 1.0572

Block length k = 2 (optimal code)
Alphabet size |Σᵏ|      :  36
Entropy H(Sᵏ)          : 4.8116 bits
Expected length E[L]   : 4.8456 bits
Average length  L̄     : 4.8420 bits
Compression ratio log₂|Σᵏ| / L̄ : 1.0677

Probability shift:  P(a)=0.30, P(f)=0.05  no re-coding
k=1  –  E[L] = 2.9500 bits   ratio = 0.8763
k=2  –  E[L] = 6.1031 bits   ratio = 0.8471
"""

# Extract k=1 values
k1_entropy = "2.4058"
k1_expected_length = "2.4500"
k1_realised_length = "2.4450"
k1_ratio = "1.0572"

# Extract k=2 values
k2_entropy = "4.8116"
k2_expected_length = "4.8456"
k2_realised_length = "4.8420"
k2_ratio = "1.0677"

# Probability shift values
shift_k1_expected_length = "2.9500"
shift_k1_ratio = "0.8763"
shift_k2_expected_length = "6.1031"
shift_k2_ratio = "0.8471"

# Generate LaTeX commands
with open("results.tex", "w") as f:
    f.write("% LaTeX commands for Huffman coding results\n")
    f.write("% Automatically generated - do not edit manually\n\n")
    
    # k=1 results
    f.write("\\newcommand{\\kOneEntropy}{" + k1_entropy + "}\n")
    f.write("\\newcommand{\\kOneExpectedLength}{" + k1_expected_length + "}\n")
    f.write("\\newcommand{\\kOneRealisedLength}{" + k1_realised_length + "}\n")
    f.write("\\newcommand{\\kOneRatio}{" + k1_ratio + "}\n\n")
    
    # k=2 results
    f.write("\\newcommand{\\kTwoEntropy}{" + k2_entropy + "}\n")
    f.write("\\newcommand{\\kTwoExpectedLength}{" + k2_expected_length + "}\n")
    f.write("\\newcommand{\\kTwoRealisedLength}{" + k2_realised_length + "}\n")
    f.write("\\newcommand{\\kTwoRatio}{" + k2_ratio + "}\n\n")
    
    # Probability shift results
    f.write("\\newcommand{\\shiftOneEL}{" + shift_k1_expected_length + "}\n")
    f.write("\\newcommand{\\shiftOneRatio}{" + shift_k1_ratio + "}\n")
    f.write("\\newcommand{\\shiftTwoEL}{" + shift_k2_expected_length + "}\n")
    f.write("\\newcommand{\\shiftTwoRatio}{" + shift_k2_ratio + "}\n")

print("results.tex generated successfully!") 