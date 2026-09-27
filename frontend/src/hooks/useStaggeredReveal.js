import { useEffect } from 'react'

export default function useStaggeredReveal() {
  useEffect(() => {
    const selectors = [
      '.school-card',
      '.be-feature',
      '.be-city-tile',
      '.be-step',
      '.be-stat-card',
      '.dashboard-school-card',
      '.be-gallery-thumb',
      '.enquiry-row',
    ]

    const elements = document.querySelectorAll(selectors.join(','))

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, idx) => {
          if (entry.isIntersecting) {
            const el = entry.target
            const siblings = Array.from(el.parentElement?.children || [])
            const siblingIndex = siblings.indexOf(el)
            const delay = Math.min(siblingIndex * 55 + Math.random() * 40, 320)

            el.style.opacity = '0'
            el.style.transform = 'translateY(18px)'
            el.style.willChange = 'transform, opacity'

            setTimeout(() => {
              el.style.transition =
                'opacity 600ms cubic-bezier(.2,.8,.2,1), transform 600ms cubic-bezier(.175,.885,.32,1.275)'
              el.style.opacity = '1'
              el.style.transform = 'translateY(0)'

              setTimeout(() => {
                el.style.transition = ''
                el.style.willChange = ''
              }, 650)
            }, delay)

            observer.unobserve(el)
          }
        })
      },
      {
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px',
      }
    )

    elements.forEach((el) => observer.observe(el))

    const mutationObserver = new MutationObserver(() => {
      document.querySelectorAll(selectors.join(',')).forEach((el) => {
        if (!el.dataset.revealObserved) {
          el.dataset.revealObserved = 'true'
          observer.observe(el)
        }
      })
    })

    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true,
    })

    return () => {
      observer.disconnect()
      mutationObserver.disconnect()
    }
  }, [])
}
