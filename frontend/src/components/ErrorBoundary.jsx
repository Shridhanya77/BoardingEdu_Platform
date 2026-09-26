import { Component } from 'react'

/**
 * Catches unexpected React render errors so users see a friendly message
 * instead of a blank screen.
 */
export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error, info) {
    // Keep console noise for developers; never show stack traces in the UI.
    console.error('BoardingEdu UI error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="container py-5 text-center">
          <h1 className="h4">Something went wrong</h1>
          <p className="text-muted">Please refresh the page or return home.</p>
          <a className="btn btn-primary btn-sm" href="/">
            Go home
          </a>
        </div>
      )
    }
    return this.props.children
  }
}
