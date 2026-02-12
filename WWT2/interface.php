<!DOCTYPE html>
<html>
    <head>
        <title>Traveling Box Man</title>
        <style>
            div {
                background-color: grey;
                align-self: center;
                width: 80pc;
                margin: 5pc;
                padding: 2pc;
                display: grid;
                place-self: center;
            }
            h2 {
                text-align: center;
                font-family: 'Futura';
                font-size: 32px;
            }
            table, th, td {
                border: 1px solid black;
            }
        </style>
    </head>
    <body style="background-color: lightgrey;">
        <h1 style="text-align: center; font-family: 'Futura'; font-size: 64px;">Traveling Box Man</h1>
        <div>
            <h2>Calculate route</h2>
        </div>
        <div>
            <h2>Current Boxes</h2>
            <table>
                <tr><th>Box ID</th><th>Box weight</th><th>Priority</th><th>Box Volume</th></tr>
                <?php
                    $fh = fopen('boxes.csv','r');
                    $count = 0;
                    while ($line = fgets($fh)) {
                        if ($count != 0) {
                            $variables = explode(',', $line);
                            echo "<tr><h4><th>".$variables[0]."</th><th>".$variables[1]."</th><th>".$variables[2]."</th><th>".$variables[3]."</h4></tr>";
                        }
                        $count++;
                    }
                    fclose($fh);
                ?>
            </table>
        </div>
        <div>
            <h2>Edit Boxes</h2>
            <h4>Remove Box with Box ID</h4>
            <form action="interface.php" method="post">
                <input type="text" name="deleteBoxId">
                <input type="submit">
            </form>
            <?php
                if ($_POST && isset($_POST['deleteBoxId'])) {
                    echo "<h4>Box ".$_POST["deleteBoxId"]." deleted</h4>";
                    shell_exec("python3 edit.py remove ".$_POST["deleteBoxId"]." 0 0 0");
                }
            ?>
            <h4>Add new box (enter ID, weight, priority, and box volume)</h4>
            <form action="interface.php" method="post">
                <input type="text" name="newBoxId">
                <input type="text" name="newBoxWeight">
                <input type="text" name="newBoxPriority">
                <input type="text" name="newBoxVolume">
                <input type="submit">
            </form>
            <?php
                if ($_POST && isset($_POST['newBoxId']) && isset($_POST['newBoxWeight'])) {
                    echo "<h4>Added box with an id of ".$_POST["newBoxId"];
                    shell_exec("python3 edit.py write ".$_POST["newBoxId"]." ".$_POST["newBoxWeight"]." ".$_POST["newBoxPriority"]." ".$_POST["newBoxVolume"]);
                }
            ?>
        </div>
        <div>
            <h2>Current Layout</h2>
        </div>
        <div>
            <h2>Edit Layout</h2>
        </div>
    </body>
</html>