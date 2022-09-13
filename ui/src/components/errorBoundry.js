import React from "react";

class ErrorBoundry extends React.Component {
    constructor(props) {
        super(props);
        this.state = {error: null, errorInfo: null};
    }

    componentDidCatch(error, errorInfo) {
        this.setState({
            error: error,
            errorInfo: errorInfo,
        });
        console.log("caught error ", error)
    }

    render(){
        if (this.state.error){
            // error has occurred
            return (
                <div>
                    <h2>Something Went Wrong</h2>
                    <details>
                        {this.state.error && this.state.error.toString()}
                        <br />
                        {this.state.errorInfo.componentStack}
                    </details>
                </div>
            );
        }
        console.log("error boundry in place")
        return this.props.children;
    }
}

export default ErrorBoundry;