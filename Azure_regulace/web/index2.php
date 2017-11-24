<html>
    <body>
        <form action="index.php" method="get">
            <input type="submit" name="f215" value="21.5">
            <input type="submit" name="f210" value="21.0">
	    <input type="submit" name="f205" value="20.5">
	    <input type="submit" name="f200" value="20.0">
       	    <input type="submit" name="f195" value="19.5">
           <input type="submit" name="EL_ON" value="ELON">
	   <input type="submit" name="EL_OFF" value="ELOFF">
      	 </form>
    </body>
</html>
<?php
$output = shell_exec('sudo python /home/pi/rs232.py');
$str     = $output;
$order   = array("/");
$replace = '<br />';

// Processes \r\n's first so they aren't converted twice.
$newstr = str_replace($order, $replace, $str);
echo $newstr;

    if(isset($_GET['f215'])) {
        f215Func();
    }
    if(isset($_GET['f195'])) {
        f195Func();
    }

    if(isset($_GET['f210'])) {
        f210Func();
    }

    if(isset($_GET['f205'])) {
        f205Func();
    }
    if(isset($_GET['f200'])) {
        f200Func();
    }

    if(isset($_GET['EL_ON'])) {
        fELONFunc();
    }
    if(isset($_GET['EL_OFF'])) {
        fELOFFFunc();
    }


 function fELONFunc(){
        echo "Button EL_ON Clicked";
        $output = shell_exec('sudo /home/pi/el_on_remote.sh');
    }
 function fELOFFFunc(){
        echo "Button EL_OFF Clicked";
        $output = shell_exec('sudo /home/pi/el_off_remote.sh');
    }




    function f215Func(){
        echo "Button 21.5 Clicked";
        $output = shell_exec('sudo python /home/pi/rs232.py 21.5');
    }
    function f195Func(){
        echo "Button 19.5 clicked";
	$output = shell_exec('sudo python /home/pi/rs232.py 19.5');
    }

    function f205Func(){
        echo "Button 20.5 clicked";
        $output = shell_exec('sudo python /home/pi/rs232.py 20.5');
    }
 
    function f200Func(){
        echo "Button 20.0 clicked";
        $output = shell_exec('sudo python /home/pi/rs232.py 20.0');
    }
    function f210Func(){
        echo "Button 21.0 clicked";
        $output = shell_exec('sudo python /home/pi/rs232.py 21.0');
    }


?>
