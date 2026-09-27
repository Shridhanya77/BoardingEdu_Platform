import { useEffect, useRef } from 'react'

export default function useMouseSpotlight(selector = '[data-spotlight]', options = {}) {
  const rafRef = useRef(null)
  const elementsRef = useRef(new Map())

  useEffect(() => {
    const interactiveSelectors = [
      '.school-card',
      '.be-feature',
      '.be-city-tile',
      '.be-step',
      '.be-stat-card',
      '.dashboard-school-card',
      ...(selector !== '[data-spotlight]' ? [selector] : []),
    ]

    const updateSpotlight = (el, clientX, clientY) => {
      const rect = el.getBoundingClientRect()
      const x = ((clientX - rect.left) / rect.width) * 100
      const y = ((clientY - rect.top) / rect.height) * 100

      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current)
      }

      rafRef.current = requestAnimationFrame(() => {
        el.style.setProperty('--mouse-x', `${Math.max(0, Math.min(100, x))}%`)
        el.style.setProperty('--mouse-y', `${Math.max(0, Math.min(100, y))}%`)
      })
    }

    const handleMouseMove = (e) => {
      const { clientX, clientY } = e

      elementsRef.current.forEach((el) => {
        const rect = el.getBoundingClientRect()
        if (
          clientX >= rect.left - 50 &&
          clientX <= rect.right + 50 &&
          clientY >= rect.top - 50 &&
          clientY <= rect.bottom + 50
        ) {
          updateSpotlight(el, clientX, clientY)
        }
      })
    }

    const attachListeners = () => {
      const allElements = document.querySelectorAll(interactiveSelectors.join(','))
      elementsRef.current.clear()

      allElements.forEach((el) => {
        if (!elementsRef.current.has(el)) {
          elementsRef.current.set(el, el)
          el.style.setProperty('--mouse-x', '50%')
          el.style.setProperty('--mouse-y', '50%')
        }
      })
    }

    attachListeners()
    document.addEventListener('mousemove', handleMouseMove, { passive: true })

    const observer = new MutationObserver(() => {
      attachListeners()
    })

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    })

    const timeoutId = setTimeout(attachListeners, 300)

    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current)
      }
      clearTimeout(timeoutId)
      document.removeEventListener('mousemove', handleMouseMove)
      observer.disconnect()
      elementsRef.current.clear()
    }
  }, [selector])
}
