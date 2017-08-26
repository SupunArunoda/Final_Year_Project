<?php
/**
 * Created by PhpStorm.
 * User: Buddhi
 * Date: 8/19/2017
 * Time: 9:27 PM
 */
require '../controller/PreprocessFileController.php';
require '../model/PreprocessFile.php';

if (isset($_POST['submit'])) {
    $file = $_FILES['inputFile'];

    if (!is_null($file)) {
        $target = '../../../data/' . $_FILES['inputFile']['name'];
        move_uploaded_file($_FILES['inputFile']['tmp_name'], $target);

        $datetime = date('Y-m-d H:i:s');
        $pf = new PreprocessFile($_FILES['inputFile']['name'], $datetime, null, null, null);

        $pfc = new PreprocessFileController();
        $res = $pfc->savePreprocessFile($pf);

        if ($res == 1) {
            echo '<script src="../../plugins/jQuery/jquery-2.2.3.min.js"></script>' .
                '<script src="../../javascript/preprocess.js"></script>' .
                '<script>runPreprocessScript(' . json_encode($file) . ')</script>';
        }

    } else {
        echo 'No file selected';
    }
}






