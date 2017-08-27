<?php

/**
 * Created by PhpStorm.
 * User: Buddhi
 * Date: 8/19/2017
 * Time: 10:33 PM
 */

require '../connection/DBConnection.php';

class PreprocessFileController
{
//    private $conn = null;
//
//    /**
//     * PreprocessFileController constructor.
//     */
//    public function __construct()
//    {
//        $dbc = new DBConnection();
//        $conn = $dbc->getConnection();
//    }

    public function savePreprocessFile(PreprocessFile $file)
    {
        $dbc = new DBConnection();
        $conn = $dbc->getConnection();
        $res = mysqli_query($conn, "INSERT INTO preprocess_file VALUES ('', '" . $file->getInputFile() . "', '" . $file->getUploadedTime() . "', '" . $file->getLastProcessStart() . "', '" . $file->getLastProcessEnd() . "', '" . $file->getOutputFile() . "')");
        mysqli_close($conn);
        return $res;
    }
}