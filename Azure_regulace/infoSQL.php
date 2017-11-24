
<?php
$serverName = "topeni.database.windows.net";
$connectionInfo = array( "Database"=>"topeni", "UID"=>"web", "PWD"=>"Laky85@@","ReturnDatesAsStrings"=>true);
$conn = sqlsrv_connect( $serverName, $connectionInfo );
if( $conn === false ) {
    die( print_r( sqlsrv_errors(), true));
}

$sql = "SELECT TOP (2) 
		DATEADD(hour,DATEPART(hour,CONVERT(time, GETUTCDATE() - CONVERT(datetime, REPLACE(CONVERT(nvarchar(16), (CAST(GETUTCDATE() AT TIME ZONE 'Central European Standard Time' AS datetimeoffset)), 127), 'T', ' '), 120))),[datum]) as datum
      ,[text]
  FROM [dbo].[logs]
  order by datum desc";
$stmt = sqlsrv_query( $conn, $sql );

if( $stmt === false) {
    die( print_r( sqlsrv_errors(), true) );
}

$row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC) ; 
     echo ("write"); 
	 echo $row['datum']."<br />";
	 echo $row['text']."<br />";

	 
echo ("start3");
sqlsrv_free_stmt( $stmt);
?>