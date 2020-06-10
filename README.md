# soft-heaps
Final research project on Soft Heaps for CS166: Data Structures, Spring 2020.

Omer Gul, Suvir Mirchandani, Charlotte Peale, Lucia Zheng

- References:
  - Bernard Chazelle. “The soft heap: an approximate priority queue with optimal error rate”. In: Journal of the ACM (JACM) 47.6 (2000), pp. 1012–1027.
  - Haim Kaplan, Robert E Tarjan, and Uri Zwick. “Soft heaps simplified”. In: SIAM Journal on Computing 42.4 (2013), pp. 1660–1673.

- Please see report in `report/final.pdf`
- Please see an interactive visualization at http://sheap.suvir.me
- Structure:
  - `sheap.py`: Python implementation of Chazelle's soft heap (adapted from Chazelle)
  - `sheap_simplified.py`: Python implementation of Kaplan et al.'s simplified soft heap (adapted from Kaplan et al.)
  - `sheap_simplified_test.py`: quick test of the simplified soft heap (adapted from Kaplan et al.)
  - `visualization.py`: visualization for the simplified soft heap and linear selection algorithms
  - `linear_select.py`: investigation into linear selection using the soft heap
  - `select_visualization.py`: quick test of the selection visualization
  - `report/`: final report
  - `viz_outputs/`
    - `exp_plots/`: results from linear select experiments
    - `select_viz/`: visualizations of linear select experiments
    - `sheap_viz/`: sample visualizations of the simplified soft heap
