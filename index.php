<?php
ob_start();

header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-cache');

ini_set('display_errors',1);
error_reporting(E_ALL ^ E_NOTICE);

set_time_limit(300);
ini_set('max_execution_time', '300');


$DIR_PYTHON = '/rsna-iaip/rsna-iaip-demo/';
$DIR_DATA = '/rsna-iaip/iaip-2023-data-samples/';
$DIR_CTP = '/rsna-iaip/apps/ctp';
$TEAMS = [
    0 => ['name'=>'bucky-john', 'folder'=>'bucky-john', 'label'=>'Bucky (Patient John)'],
    1 => ['name'=>'bucky-david', 'folder'=>'bucky-david-priors', 'label'=>'Bucky (Patient David - PRIORS)'],
    2 => ['name'=>'bucky-david', 'folder'=>'bucky-david-current', 'label'=>'Bucky (Patient David - CURRENTS)'],
    3 => ['name'=>'mallard', 'folder'=>'mallard', 'label'=>'Mallard'],
    4 => ['name'=>'jensen', 'folder'=>'jensen', 'label'=>'Jensen'],
];
?>
<html>
<head>
	<title>RSNA Imaging AI in Practice Demonstration</title>
    <h1>Demo Data Generator Self-Serve</h1>
	
	<!-- BOOTSTRAP -->
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
	<!-- Optional theme -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
	<!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</head>
<body style="padding: 15px; width: 100%;">
    <?php

    function is_running()
    {
        $pid_cpt = shell_exec("ps fax | grep -v 'grep' | grep CTP | head -n1 | sed 's/^ *//g' | cut -f 1 -d ' '");
        $pid_storescu = shell_exec("ps fax | grep -v 'grep' | grep storescu | head -n1 | sed 's/^ *//g' | cut -f 1 -d ' '");
        $pid_stowrs = shell_exec("ps fax | grep -v 'grep' | grep stowrs | head -n1 | sed 's/^ *//g' | cut -f 1 -d ' '");
        //print("pid_cpt={$pid_cpt} pid_storescu={$pid_storescu} pid_stowrs={$pid_stowrs} \n");
        
        if( $pid_cpt != '' || $pid_storescu != '' || $pid_stowrs != '' ) {
            return true;
        }
        return false;
    }
    $is_running = is_running();
    $diabled = $is_running ? 'disabled="true"':'';
    $mode = array_key_exists('mode', $_REQUEST) ? $_REQUEST['mode']:'';
    $team_id = array_key_exists('team_id', $_REQUEST) ? intval($_REQUEST['team_id']):0;
    $new_demographics = array_key_exists('new_demographics', $_REQUEST);
    $months_offset = array_key_exists('months_offset', $_REQUEST) ? intval($_REQUEST['months_offset']):0;
    

    switch( $mode )
    {
        case 'run':
            if( $is_running )
            {
                echo "<div class='alert alert-error'>Sorry - request failed due to another session that got started by someone else.</div>\n";
                break;
            }
            if( !in_array($team_id, array_keys($TEAMS)) )
            {
                echo "<div class='alert alert-error'>Sorry - Unkown team!!</div>\n";
                break;
            }
            $team = $TEAMS[$team_id];
            echo "<p>About to kick-off a demo dataset - please hold for the patient name and MRN</p>";
            ob_flush();
            flush();

            // Kick off the generator
            $cmd = "cd {$DIR_PYTHON}; python main.py -c {$DIR_CTP} -t {$team['name']} -l './logs' -d {$DIR_DATA}{$team['folder']}";
            if( $new_demographics ) {
                $cmd .= " -nd True";
            }
            if( $months_offset > 0 ) {
                $cmd .= " -m " . $months_offset;
            }
            //echo "{$cmd}<br />\n";

            $output = shell_exec($cmd);
            //var_export($output);
            
            $lines = explode("\n", $output != null ? $output:'');
            foreach( $lines as $line )
            {
                if( strpos($line, 'Patient name') > 0 ) 
                {
                    echo "<p>{$line}</p>\n";
                }
            }
            echo "<div class='alert alert-success'>Success! Generated a dataset for {$team['label']}</div>\n";
            break;
    }

    if( is_running() ) 
    {
        echo "<div class='alert alert-warning'>Warning: Another data generation session is already in progress. Please wait a bit, then refresh to start another session</div>\n";
    }
    ?>
    <h2>Generate a new set</h2>
    <form action="?" method="POST">
        <p>Which team do you want to generate data for?</p>
        <?php
            foreach( $TEAMS as $index => $team )
            {
                echo "<input type='radio' name='team_id' id='{$team['folder']}' value='{$index}' /> <label for={$team['folder']}>{$team['label']}</label><br />\n";
            }
        ?>

    <input type="checkbox" id="new_demographics" name="new_demographics" value="true" checked="true" />&nbsp;<label for="new_demographics">Generate new demographics?</label><br />
    <p>If checked, new patient demographics will be generated (name, MRN). Otherwise, the demographics from the last run will be used (useful for generating priors and currents)</p>

    <label for="months_offset">Months offset</label>&nbsp;<input type="text" name="months_offset" id="months_offset" value="0" /><br />
    <p>When generating priors, enter a value like &quot;9&quot; to give them a study date from nine months ago. Otherwise, leave it at zero for today&apos;s date.</p>

    <input type="hidden" name="mode" value="run" />
    <input type="submit" name="submit" value="Submit" class="btn btn-primary" <?php echo $diabled; ?> />
    <p>Warning: Once you submit, the page may take a full minute or two before it loads, please hold for the patient name and MRN.</p>

</body>
</html>
<?php
ob_end_flush(); 
?>