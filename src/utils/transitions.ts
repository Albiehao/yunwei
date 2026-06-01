/**
 * Page transition variants for Vue Router
 * Creates a staggered fade-in effect for page content
 */
export const pageTransition = {
  name: 'page-fade',
  mode: 'out-in' as const
}

export const pageTransitionClasses = {
  enterActiveClass: 'page-enter-active',
  leaveActiveClass: 'page-leave-active',
  enterFromClass: 'page-enter-from',
  leaveToClass: 'page-leave-to',
}
