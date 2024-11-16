console.log('Script is running');

const canvas = document.getElementById('avlCanvas');
const ctx = canvas.getContext('2d');

ctx.fillStyle = 'green';
ctx.fillRect(10, 10, 50, 50); // Draw a green rectangle to test

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('avlCanvas');
    const ctx = canvas.getContext('2d');

    function drawNode(x, y, value, color) {
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = 'black';
        ctx.fillText(value, x - 5, y + 5);
    }

    drawNode(100, 100, 'A', 'blue'); // Test drawing a node
});



// const canvas = document.getElementById('avlCanvas');
// const ctx = canvas.getContext('2d');


// ctx.fillStyle = 'green';
// ctx.fillRect(10, 10, 50, 50); // Draw a green rectangle to test


// function drawNode(x, y, value, color) {
//     console.log(`Drawing node at (${x}, ${y}) with value ${value}`);
//     ctx.beginPath();
//     ctx.arc(x, y, 20, 0, 2 * Math.PI);
//     ctx.fillStyle = color;
//     ctx.fill();
//     ctx.stroke();
//     ctx.fillStyle = 'black';
//     ctx.fillText(value, x - 5, y + 5);
// }

// function drawEdge(x1, y1, x2, y2) {
//     ctx.beginPath();
//     ctx.moveTo(x1, y1);
//     ctx.lineTo(x2, y2);
//     ctx.stroke();
// }

// function animateInsertion(node, parent, x, y, color) {
//     drawNode(x, y, node.value, color);
//     if (parent) {
//         drawEdge(parent.x, parent.y, x, y);
//     }
//     setTimeout(() => {
//         // Update the AVL tree structure and re-draw
//     }, 1000);
// }

// async function fetchCsvFiles(folderPath) {
//     const response = await fetch(folderPath);
//     const files = await response.json();
//     return files;
// }

// async function processCsvData(folderPath) {
//     const files = await fetchCsvFiles(folderPath);
//     const graph = new nx.Graph();

//     for (const file of files) {
//         const response = await fetch(`${folderPath}/${file}`);
//         const csvText = await response.text();
//         const rows = csvText.split('\n').map(row => row.split(','));

//         const color = file === files[files.length - 1] ? 'red' : 'blue';

//         rows.forEach(row => {
//             if (row.length === 3) {
//                 const [id, x, y] = row;
//                 graph.addNode(id, { x: parseFloat(x), y: parseFloat(y), color: color });
//             } else if (row.length === 2) {
//                 const [source, target] = row;
//                 graph.addEdge(source, target);
//             }
//         });
//     }
//     return graph;
// }

// function drawGraph(graph) {
//     graph.nodes.forEach(node => {
//         drawNode(node.x, node.y, node.id, node.color);
//     });
//     graph.edges.forEach(edge => {
//         const source = graph.getNode(edge.source_id);
//         const target = graph.getNode(edge.target_id);
//         drawEdge(source.x, source.y, target.x, target.y);
//     });
// }

// (async function() {
//     const folderPath = '/home/rm_subhiksha/LAM_SRM/Graph_Generator/trial1'; // Update this path
//     const graph = await processCsvData(folderPath);
//     drawGraph(graph);
// })();
