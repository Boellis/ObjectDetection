-----------------------------------
          Table of Contents
-----------------------------------
1. Setting Up Tensorflow Environment
2. Tensorboard
   tensorboard --logdir=c:/users/boellis/patdetection
   localhost
3. Fill
4. Setting up Object Detection API
    i.    Collecting Images
    ii.   Creating a Label Map
    iii.  Labeling Images with LabelImg
    iv.   Converting XML files to CSV
    v.    Generating TFRecord file from CSV
    vi.   Modifying the Config file
    vii.  Training
    viii. Saving Checkpoint Model(.ckpt) as a .pb File
    ix.   Using model in your project
    x.

    4-ii. Label Map
      1. Creating a label map
          a.
          Open up one of your favorite text editors and follow the format below to setup labels:
          #Do not start with 0. You start with one. You need no explanation. Cool, here it is

          item {
            id: 1
            name: 'sprite'
          }
          b.
          Save your label map in the format class_label_map.pbtxt, where 'class' indicates the association amongst the labels

   4-iii. LabelImg
      1. Setting Up LabelImg & Annotating Images
          a.
          Follow the instructions on the github page to setup LabelImg on your computer. https://github.com/tzutalin/labelImg
          Download prebuilt binaries(windows 1.6)
          b.
          Once you have LabelImg cloned onto your computer, go to the file folder and run the .exe file.
          c.
          When LabelImg opens, select 'Open Dir' and navigate to the file folder containing all of your .jpg and .png files.
          d.
          After selecting the folder, the first image file should appear on your screen. Check the 'Use default label' and enter the label you want to annotate with. This will annotate each image you box with the selected label.
          e.
          It's a pain in the butt labeling all these images, so using hotkeys helps a ton.
          w - draw box
          d - next image
          space - verify & save image

    4-iv. Converting XML files to CSV
      1.  Configuring your xml_to_csv.py
          a.
          Copy the xml_to_csv.py file from the cloned repository.
          b.
          In the main function, 'image_path' dictates where your xml files will be read from. Create a folder called 'data' in the same folder as your xml_to_csv.py script. This will be where your .csv files will be stored from the python script.
          To make sure this is set up correctly, create a folder called 'images' in the same folder as your xml_to_csv.py script. Within the images folder, create two separate folders called 'train' and 'test'. These are the folders that your .xml files should be in, and will also be where the xml_to_csv.py will read from.
          c.
          Once your folders are set up correctly, open the terminal and navigate to the file folder containing your xml_to_csv.py script and run the following command in your prompt: 'python xml_to_csv.py'.
          d.
          Your new files are now in your 'data' folder, but there's still work to be done. Navigate to your 'data' folder and locate your new train_labels and test_labels files. Select them and add .csv to the end of each to change them to .csv files.

     4-v. Generating TFRecord file from CSV
      1. Configuring our generate_tfrecord.py script
         a.
         Kudos to you for making it this far in. Go ahead and copy generate_tfrecord.py and paste it into the same folder as your xml_to_csv.py script. Go ahead and open that bad boy up in an editor of your choice.
         b.
         Depending on the labels we have in our label map, we want to format the 'class_text_to_int' function to accept our labels and be a happy program. A template for setting up multiple labels exists in the comments above the 'class_text_to_int' function. Use elif's to add as many labels as you'd like.
         Save that bad boy and move on to the next step.
         c.
         Now we're ready to run, so lets go ahead and go back to our terminal. Navigate back to your file folder containing your generate_tfrecord.py script. We're going to be running two instances of our script, each with different parameters. Our --csv_input will point towards our .csv files we just created. Our --output_path will point to the file folder where our .record files will be generated to and stored. The usage format for running the script is located in the comments of generate_tfrecord.py
         d.
         Run the python script following the usage template located in the file.

   4-vi. Modifying the Config file
      1. Configuring our dataset.config file to correspond to our new Model
         a.
         Navigate to object_detection/samples/configs to find config files for pre-trained models. Select a model that best fits the task you're looking to accomplish.
         b.
         Copy the config file into the same folder as your generate_tfrecord.py script. In this folder create a folder called 'models'  and move the .cpkt(checkpoint) files (3 of them) of the pre-trained model you selected into this folder.

         Here are links to a few pretrained models:

         Pretrained Models on Tensorflow Github:  https://github.com/tensorflow/models/tree/master/research/object_detection/samples/configs

         More Pretrained models:
         https://github.com/tensorflow/models/tree/master/research/slim
         c.
         Inside our models folder, create a folder 'train'
         d.
         Open up your .config file  and change the num_classes number to correspond to the amount of labels you have in your label map.
         e.
         In your .config file, change the fine_tune_checkpoint path to point to the model.ckpt file.
         fine_tune_checkpoint: "models/model.ckpt"
         f.
         In your .config file, change the input_path and label_map_path for both the train and test dataset.
            train_input_reader{
              input_path: "data/train.record"
              label_map_path: "data/soda_label_map.pbtxt"
            }

            eval_input_reader{
              input_path: "data/test.record"
              label_map_path: "data/soda_label_map.pbtxt"
            }
         g. Now we're ready to train

  4-vii. Training
      1. Training
         a.
         Navigate to the folder containing your train.py script and run the following command:
         python train.py --logtostderr --train_dir=./models/train --pipeline_config_path=ssd_mobilenet_v1_coco.config
         b.
         All your training stuff will be placed in "models/train" folder
         c.
         Set the pipeline_config_path= c:/users/boellis/desktop/patdetection/models/train/pipeline.config

4-viii. Saving Checkpoint Model(.ckpt) as a .pb File
     1.
        a.
        Copy the export_inference_graph.py script from the repo and paste it into the folder containing your other python files.
        b.
        Navigate to the folder containing your export_inference_graph.py script and run the following command:
        python export_inference_graph.py --input_type image_tensor --pipeline_config_path ./ssd_mobilenet_v1_coco.config --trained_checkpoint_prefix ./models/train/model.ckpt-5000 --output_directory ./fine_tuned_model
           i. Your input_type will not change,
          ii. Your pipeline_config_path should point to your modified config file,
         iii. Your trained_checkpoint_prefix should point to your trained model
          iv. Your output_directory should point to the file folder where your .pb file will be created and stored from the script.
        c.
