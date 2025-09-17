# TODO List for Udacity Pet Image Classification Project

## Step 1: Implement get_input_args.py ✅
- Add argparse setup for --dir, --arch, --dogfile with defaults
- Return parser.parse_args()

## Step 2: Implement get_pet_labels.py ✅
- Extract pet labels from filenames (e.g., 'Boston_terrier_02259.jpg' -> 'boston terrier')
- Create results_dic with filename as key and [pet_label] as value
- Handle duplicates and skip hidden files

## Step 3: Implement classify_images.py ✅
- Use classifier function to get model labels
- Process labels to lowercase and strip whitespace
- Compare pet labels with classifier labels and update results_dic with [pet_label, classifier_label, match(1/0)]

## Step 4: Implement adjust_results4_isadog.py ✅
- Read dognames.txt
- Add is_dog flags for pet and classifier labels
- Update results_dic with dog classification

## Step 5: Implement calculates_results_stats.py ✅
- Calculate counts and percentages for matches, dog classifications, etc.
- Return results_stats dictionary

## Step 6: Implement print_results.py ✅
- Print summary results, incorrect classifications

## Step 7: Update check_images.py ✅
- Fix function calls to pass correct arguments (in_arg.dir, in_arg.arch, in_arg.dogfile)
- Ensure timing is implemented

## Step 8: Test the program ✅
- Run with default arguments
- Run with custom arguments
- Verify output matches rubric
