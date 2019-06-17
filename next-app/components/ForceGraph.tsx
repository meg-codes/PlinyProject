import * as React from 'react';
import * as d3 from 'd3';

type ForceGraphProps = {
  width: number,
  height: number,
  id: string,
  title: string
}

type ForceGraphState = {
  simulation: any
}

export default class ForceGraph extends React.Component<ForceGraphProps, ForceGraphState> {

  simulation: d3.Simulation

  constructor(props: ForceGraphProps) {
    super(props);  
  }

  async componentDidMount() {
    const data = await d3.json('/people/nodes.json')
    const links = data.links.map(d => Object.create(d));
    const nodes = data.nodes.map(d => Object.create(d));

    const setColor = (d) => {
      var colors = {
          0: 'gray',
          'citizen': 'aquamarine',
          'equestrian': 'green',
          'sentorial': 'purple',
          'consular': 'indigo',
      };

      return colors[d.group];
  
  }

    const drag = simulation => {
  
      function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }
      
      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }
      
      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
      
      return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
    }
  


    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-500))
        .force("center", d3.forceCenter(this.props.width / 2, this.props.height / 2));
    
    this.simulation = simulation;

    const svg = d3.select('svg')
    
    svg.append('rect')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('fill', 'grey')
  
    const link = svg.append("g")
        .attr("stroke", "black")
        .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));
  
    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
        .attr("r", 8)
        .attr("fill", (d) => setColor(d))
        .attr("role", "img")
        .attr("tabindex", "-1")
        .call(drag(simulation))
  
    const title = node.append("title")
        title.append('span')
        .attr('lang', 'la')
        .text(d => d.id)

        title.append('span')
        .text(d => {
          return 
        })

    simulation.on("tick", () => {
      link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
  
      node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
    });
    

    const circles = document.querySelectorAll('circle')
    let i = -1;
    d3.select('svg').on("keydown", () => {
      console.log(d3.event)
      if (d3.event.key === "ArrowDown" && d3.event.shiftKey === true) {
          if (i < circles.length - 1) {
            i++
          } else {
            i = 0;
          }
          circles[i].focus()
        }
      if (d3.event.key === "ArrowUp" && d3.event.shiftKey === true) {
        if (i > 0) {
          i-- } else {
            i = circles.length - 1;
          }
        circles[i].focus()
      }
    })

  }

  componentWillUnmount() {
    this.simulation.stop()
  }

  render() {
    return (
      <svg role="group" id={this.props.id} width={this.props.width} 
      height={this.props.height} tabIndex='0'>
        <title id={`${this.props.id}_title`}>{this.props.title}</title>
      </svg>
    )
  }

}