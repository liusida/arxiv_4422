<!DOCTYPE html>
<html>
<?php
$bgscale = 8.485;
?>

<head>
    <meta charset='utf-8'>
    <title>Deep Learning</title>
    <script src="https://d3js.org/d3.v6.min.js"></script>
    <script src="detect-zoom.js"></script>
    <style>
        #intro {
            font-size: 20px;
        }
        #intro .title {
            font-weight: bold;
        }
        #intro .img {
            padding-left: 100px;
        }
        #intro .img img {
            border: 1px solid black;
        }
        #main {
            /* border: 1px solid red; */
            position: relative;
            overflow: hidden;
            height: 53300px;
        }

        #bg {
            position: absolute;
            top: 6px;
            left: 5px;
            height: <?php echo 4422 * $bgscale ?>px;
            width: <?php echo 4422 * $bgscale ?>px;
            background-image: url('bg.png');
            background-size: <?php echo 4422 * $bgscale ?>px;
            transform-origin: top left;
            transform: rotate(45deg);
            z-index: -1;
        }

        #list {
            padding-top: 20px;
            padding-left: 0px;
            margin-left: 500px;
            position: relative;
        }

        #list div {
            position: absolute;
            top: 0px;
            left: 0px;
            margin-left: 0px;
            padding-left: 0px;
            line-height: 13px;
            font-size: 8px;
            white-space: nowrap;
            background-color: white;
            cursor: pointer;
        }

        #arxiv_tooltip {
            border: 1px solid black;
            background-color: white;
            position: absolute;
            top: -1000px;
            left: -1000px;
            width: 500px;
            /* height: 200px; */
            padding: 20px;
        }

        #arrow {
            color: red;
            font-size: 20px;
            position: absolute;
            top: -1000px;
            left: 0px;
        }

    </style>

    <script>
        document.addEventListener("DOMContentLoaded", function(event) {
            // return;
            d3.selectAll(".paper").style("top", function() {
                    let _top = parseInt(parseFloat(d3.select(this).attr('index') * 12));
                    return _top + "px";
                })
                .on("mousemove", function(d) {
                    let _arxiv_id = d3.select(this).attr("arxiv_id");
                    let _tooltip = d3.select(this).attr("tooltip");
                    let _top = parseInt(parseFloat(d3.select(this).attr('index') * 12));

                    d3.select("#arxiv_tooltip")
                        .style("font-size", parseInt(20 / detectZoom.zoom())+"px")
                        .style("width", parseInt(500 / detectZoom.zoom())+"px")
                        .style("top", (_top+20) + "px")
                        .style("left", d.pageX + "px")
                        .html(_tooltip);
                    
                    d3.select("#arrow")
                        .style("top", _top + "px");

                })
                .on("mouseout", function(){
                    d3.select("#arxiv_tooltip")
                        .style("top", "-1000px")
                })
                .on("click", function(d) {
                    let _arxiv_id = d3.select(this).attr("arxiv_id");
                    window.open("https://arxiv.org/abs/"+_arxiv_id, "_blank");
                });


        });
    </script>

</head>

<body>
    <div id="intro">
        <p class="title">Exploring Highly Cited arXiv Deep Learning Papers</p>
        <p>This list shows 4,422 highly cited arXiv papers in two subcategories: cs.LG and cs.AI retrived in April, 2021.</p>
        <p>The order of the list is arranged so that papers with stronger relationships are placed closer to each other.</p>
        <p>Here is a preview of the entire matrix. The most famous authors are usually in the middle of the list.</p>
        <div class="img"><a href="bg.png" target="_blank"><img src="bg.png" width="400" height="400"></a></div>
        <p>For more information, please refer to: <a href="https://github.com/liusida/arxiv_4422">https://github.com/liusida/arxiv_4422</a>
        <p>The detailed list starts here:</p>
    </div>
    <div id="main">
        <div id="bg">
        </div>
        <div id="list">
            <?php include 'the_page.html'; ?>
        </div>
        <div id="arxiv_tooltip"></div>
        <div id="arrow">➞</div>
    </div>
</body>

</html>