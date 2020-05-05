html>
<head>
    <title>Covid-19 Data</title>
</head>
<body>
<table align="center" border="1">
<?php
    $cnx = new mysqli('localhost', 'AGuy', 'Arcane233', 'CovCases');

    if ($cnx->connect_error)
        die('Connection failed: ' . $cnx->connect_error);

    $query = 'SELECT * FROM covcases';
    $cursor = $cnx->query($query);
    while ($row = $cursor->fetch_assoc()) {
        echo '<tr>';
        echo '<td>' . $row['State'] . '</td><td>' . $row['Cases'] . '</td><td align="right">' . $row['Deaths'] .'</td>';
        echo '</tr>';
    }

    $cnx->close();
?>
</table>
</body>
</html>
