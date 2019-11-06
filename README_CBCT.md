# Setup environment

- Install virtualenv
- Create virtual environment with python3:
    ```
	virtualenv --system-side-packages -p python3 ./venv3
    ```
- Activate virtual env
    ```
	source ./venv3/bin/activate
    ```
- Clone repo
    ```
	git clone https://github.com/naeims/tf_unet
	cd tf_unet
    ```
- Install required packages
	```
    pip install -r requirements.txt
    ```
- Install this package in developer mode (points to local dir)
    ```
	python setup.py develop --user
    ```
- Add virtual env to jupyter
    ```
	python -m ipykernel install --user --name=venv3
    ```
- Run jupyter
    ```
	jupyter notebook
    ```


# Data pipeline:

* prepare_dcm_files.sh
    * Input: dcm_raw, mapping.csv
    * Output: dcm
	* Purpose:
	    * Removes all slices marked as garbage

* prepare_png_files.sh
	* Input: dcm
	* Output: jpg, png, png_color
	* Purpose:
		* jpg is used by classifier
		* png is used by localizer
		* png_color is used by radiologist to demarcate CACs (same as labels_raw)

* prepare_classifier_data.sh
	* Input: jpg, mapping.csv
	* Output: classifier_training
	* Purpose:
		* Splits the data into cbctno and cbctyes categories

* prepare_localizer_data.sh
	* Input: labels_raw, png, mapping.csv
	* Output: localizer_training/all and /positive

# Training the classifier

* retrain.sh
	* Input: classifier_training, # training steps
	* Output: retrained_graph.pb, retrained_labels.txt

# Testing the classifier

* test_all_files_fast.sh
	* Input: jpg
	* Output: results.csv, results_backup.csv
	* Purpose:
		* Assigns a yesness to every slice, stores results.csv

* calculate_yes_boundaries.sh
	* Input: results.csv
	* Output: yes_boundaries.csv
	* Purpose:
		* Fits a step function to find best boundary

* report_error_of_classifier.sh
	* Input: mapping.csv, yes_boundaries.csv
	* Output: A number
	* Purpose:
		* Report how well the classifier did

# Training the localizer
* Run jupyter notebook
* Open localizer_training

# Testing the localizer
* Run jupyter notebook
* Open localizer_testing
