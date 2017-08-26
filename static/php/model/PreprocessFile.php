<?php

/**
 * Created by PhpStorm.
 * User: Buddhi
 * Date: 8/19/2017
 * Time: 10:32 PM
 */
class PreprocessFile
{
    private $input_file;
    private $uploaded_time;
    private $last_process_start;
    private $last_process_end;
    private $output_file;

    /**
     * PreprocessFile constructor.
     * @param $input_file
     * @param $uploaded_time
     * @param $last_process_start
     * @param $last_process_end
     * @param $output_file
     */
    public function __construct($input_file, $uploaded_time, $last_process_start, $last_process_end, $output_file)
    {
        $this->input_file = $input_file;
        $this->uploaded_time = $uploaded_time;
        $this->last_process_start = $last_process_start;
        $this->last_process_end = $last_process_end;
        $this->output_file = $output_file;
    }

    /**
     * @return mixed
     */
    public function getInputFile()
    {
        return $this->input_file;
    }

    /**
     * @param mixed $input_file
     */
    public function setInputFile($input_file)
    {
        $this->input_file = $input_file;
    }

    /**
     * @return mixed
     */
    public function getUploadedTime()
    {
        return $this->uploaded_time;
    }

    /**
     * @param mixed $uploaded_time
     */
    public function setUploadedTime($uploaded_time)
    {
        $this->uploaded_time = $uploaded_time;
    }

    /**
     * @return mixed
     */
    public function getLastProcessStart()
    {
        return $this->last_process_start;
    }

    /**
     * @param mixed $last_process_start
     */
    public function setLastProcessStart($last_process_start)
    {
        $this->last_process_start = $last_process_start;
    }

    /**
     * @return mixed
     */
    public function getLastProcessEnd()
    {
        return $this->last_process_end;
    }

    /**
     * @param mixed $last_process_end
     */
    public function setLastProcessEnd($last_process_end)
    {
        $this->last_process_end = $last_process_end;
    }

    /**
     * @return mixed
     */
    public function getOutputFile()
    {
        return $this->output_file;
    }

    /**
     * @param mixed $output_file
     */
    public function setOutputFile($output_file)
    {
        $this->output_file = $output_file;
    }
}