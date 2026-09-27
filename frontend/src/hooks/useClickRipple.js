import { useEffect } from 'react'

export default function useClickRipple() {
  useEffect(() => {
    const createRipple = (e) => {
      const target = e.target.closest('.btn, .be-city-tile, .be-chip, .school-card, .be-feature, .be-step, .be-stat-card, .dashboard-school-card')
      if (!target) return

      const rect = target.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height) * 1.5
      const x = e.clientX - rect.left - size / 2
      const y = e.clientY - rect.top - size / 2

      const ripple = document.createElement('span')
      ripple.style.cssText = `
        position: absolute;
        left: ${x}px;
        top: ${y}px;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0) 70%);
        pointer-events: none;
        transform: scale(0);
        animation: rippleExpand 650ms ease-out forwards;
        z-index: 999;
      `

      const computedStyle = getComputedStyle(target)
      if (computedStyle.position === 'static') {
        target.style.position = 'relative'
      }
      target.style.overflow = 'hidden'
      target.appendChild(ripple)

      setTimeout(() => ripple.remove(), 700)
    }

    const styleId = 'ripple-keyframe-style'
    if (!document.getElementById(styleId)) {
      const style = document.createElement('style')
      style.id = styleId
      style.textContent = `
        @keyframes rippleExpand {
          0% {
            transform: scale(0);
            opacity: 1;
          }
          100% {
            transform: scale(1);
            opacity: 0;
          }
        }
      `
      document.head.appendChild(style)
    }

    document.addEventListener('click', createRipple, { passive: true })
    return () => document.removeEventListener('click', createRipple)
  }, [])
}
