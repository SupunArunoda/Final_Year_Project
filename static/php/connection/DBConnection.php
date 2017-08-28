<?php

/**
 * Created by PhpStorm.
 * User: Buddhi
 * Date: 8/19/2017
 * Time: 9:33 PM
 */
class DBConnection
{
    function getConnection()
    {
        $servername = "localhost";
        $username = "root";
        $password = "";
        $database = "adist";

        $conn = mysqli_connect($servername, $username, $password, $database);

        if ($conn->connect_error) {
            return $conn->connect_error;
        } else {
            return $conn;
        }

    }
}