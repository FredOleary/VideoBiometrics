import React from 'react';

const modalButton = {
  marginLeft:'30px',
  marginRight:'auto',
  marginTop:'20px',
  marginBottom:'auto',
  textAlign:'center',
  height:30, 
  fontSize:'16px'
};


class ModalDialog extends React.Component {

  render() {
    return (
        <div>
          <h2>{this.props.title}</h2>
          <div>{this.props.subject}</div>
          <div>
            <button style={modalButton} onClick={this.props.closeModal}>Yes</button>
            <button style={modalButton} onClick={this.props.cancelModal}>No</button>
          </div>
        </div>
    );
  }
}

export default ModalDialog;
