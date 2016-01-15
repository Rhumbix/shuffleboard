'use strict'

var Score = React.createClass({
  scores: function() {
    var that = this;
    $.ajax({
      url: '/score',
      dataType: 'json',
      cache: false,
      success: function(data) {
        that.setState(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
        this.setState({red: 999, blue: 999});
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {red: 0, blue: 0};
  },
  componentDidMount: function() {
    setInterval(this.scores, 10000);
    this.scores();
  },
  render: function() {
    return (
      <div>
        <h2>Red: {this.state.red}</h2>
        <h2>Blue: {this.state.blue}</h2>
      </div>
    );
  }
});

React.render(
  <Score />,
  document.getElementById('score')
);
