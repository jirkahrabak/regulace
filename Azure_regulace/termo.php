<?php
//echo 'Hello ' . htmlspecialchars($_GET[""]) . '!';
//print_r($_GET);

// Write the contents to the file, 
// using the FILE_APPEND flag to append the content to the end of the file
// and the LOCK_EX flag to prevent anyone else writing to the file at the same time
echo 'test';
$bigArray = array_values( $_GET );
$a= $bigArray[0];
echo $a;
$file = fopen("test.txt","w") or die("Unable to open file!");
fwrite($file,$a);
fclose($file);

//$myfile = fopen("test.txt", "r") or die("Unable to open file!");
//echo fread($myfile,filesize("test.txt"));
//fclose($myfile);
?>
