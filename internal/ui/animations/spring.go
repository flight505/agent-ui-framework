// Package animations provides smooth animation utilities using spring physics.
package animations

import (
	"time"

	"github.com/charmbracelet/harmonica"
	tea "github.com/charmbracelet/bubbletea"
)

// Spring wraps harmonica.Spring with Bubbletea integration.
type Spring struct {
	spring   harmonica.Spring
	target   float64
	current  float64
	velocity float64
	active   bool
}

// SpringConfig defines spring physics parameters.
type SpringConfig struct {
	FPS       int     // Frames per second (default: 60)
	Stiffness float64 // Spring stiffness (default: 7.0, range: 1-20)
	Damping   float64 // Spring damping (default: 0.15, range: 0.05-1.0)
}

// DefaultSpringConfig returns sensible defaults for Charm aesthetic.
// These values create smooth, responsive animations (200-300ms duration).
func DefaultSpringConfig() SpringConfig {
	return SpringConfig{
		FPS:       60,
		Stiffness: 7.0,  // Moderate spring for snappy feel
		Damping:   0.15, // Low damping for smooth motion
	}
}

// FastSpringConfig returns config for fast micro-interactions (~100ms).
func FastSpringConfig() SpringConfig {
	return SpringConfig{
		FPS:       60,
		Stiffness: 12.0, // Higher stiffness = faster
		Damping:   0.25, // More damping to prevent overshoot
	}
}

// SlowSpringConfig returns config for deliberate transitions (~500ms).
func SlowSpringConfig() SpringConfig {
	return SpringConfig{
		FPS:       60,
		Stiffness: 4.0,  // Lower stiffness = slower
		Damping:   0.1,  // Less damping for more natural motion
	}
}

// NewSpring creates a new spring animator.
func NewSpring(config SpringConfig) *Spring {
	return &Spring{
		spring:   harmonica.NewSpring(harmonica.FPS(config.FPS), config.Stiffness, config.Damping),
		current:  0,
		target:   0,
		velocity: 0,
		active:   false,
	}
}

// SetTarget sets a new target value and activates the spring.
func (s *Spring) SetTarget(target float64) {
	s.target = target
	s.active = true
}

// SetCurrent immediately sets the current value (no animation).
func (s *Spring) SetCurrent(value float64) {
	s.current = value
	s.target = value
	s.velocity = 0
	s.active = false
}

// Update advances the spring by one frame.
// Returns true if still animating.
func (s *Spring) Update() bool {
	if !s.active {
		return false
	}

	s.current, s.velocity = s.spring.Update(s.current, s.velocity, s.target)

	// Stop if settled (within 0.5 of target with low velocity)
	if isSettled(s.current, s.velocity, s.target, 0.5) {
		s.current = s.target
		s.velocity = 0
		s.active = false
		return false
	}

	return true
}

// isSettled checks if a spring has settled to its target.
func isSettled(current, velocity, target, threshold float64) bool {
	// Check if position is close to target and velocity is low
	positionDelta := current - target
	if positionDelta < 0 {
		positionDelta = -positionDelta
	}

	if velocity < 0 {
		velocity = -velocity
	}

	return positionDelta < threshold && velocity < threshold
}

// Value returns the current spring value.
func (s *Spring) Value() float64 {
	return s.current
}

// IsActive returns true if the spring is currently animating.
func (s *Spring) IsActive() bool {
	return s.active
}

// TickMsg is sent by the spring to trigger animation updates.
type TickMsg time.Time

// TickCmd returns a command that sends TickMsg at spring FPS.
func TickCmd() tea.Cmd {
	return tea.Tick(time.Second/60, func(t time.Time) tea.Msg {
		return TickMsg(t)
	})
}

// PositionSpring animates vertical/horizontal position.
type PositionSpring struct {
	X *Spring
	Y *Spring
}

// NewPositionSpring creates a spring for 2D positioning.
func NewPositionSpring(config SpringConfig) *PositionSpring {
	return &PositionSpring{
		X: NewSpring(config),
		Y: NewSpring(config),
	}
}

// SetTarget sets target X,Y coordinates.
func (p *PositionSpring) SetTarget(x, y float64) {
	p.X.SetTarget(x)
	p.Y.SetTarget(y)
}

// SetCurrent immediately sets current position.
func (p *PositionSpring) SetCurrent(x, y float64) {
	p.X.SetCurrent(x)
	p.Y.SetCurrent(y)
}

// Update advances both springs.
func (p *PositionSpring) Update() bool {
	xActive := p.X.Update()
	yActive := p.Y.Update()
	return xActive || yActive
}

// Position returns current X,Y coordinates as integers.
func (p *PositionSpring) Position() (int, int) {
	return int(p.X.Value()), int(p.Y.Value())
}

// IsActive returns true if either spring is animating.
func (p *PositionSpring) IsActive() bool {
	return p.X.IsActive() || p.Y.IsActive()
}

// OpacitySpring animates opacity (0.0 - 1.0).
type OpacitySpring struct {
	spring *Spring
}

// NewOpacitySpring creates a spring for fade animations.
func NewOpacitySpring(config SpringConfig) *OpacitySpring {
	return &OpacitySpring{
		spring: NewSpring(config),
	}
}

// FadeIn sets target to 1.0 (fully visible).
func (o *OpacitySpring) FadeIn() {
	o.spring.SetTarget(1.0)
}

// FadeOut sets target to 0.0 (fully transparent).
func (o *OpacitySpring) FadeOut() {
	o.spring.SetTarget(0.0)
}

// SetOpacity sets target opacity (0.0 - 1.0).
func (o *OpacitySpring) SetOpacity(opacity float64) {
	if opacity < 0.0 {
		opacity = 0.0
	}
	if opacity > 1.0 {
		opacity = 1.0
	}
	o.spring.SetTarget(opacity)
}

// Update advances the opacity spring.
func (o *OpacitySpring) Update() bool {
	return o.spring.Update()
}

// Opacity returns current opacity value (0.0 - 1.0).
func (o *OpacitySpring) Opacity() float64 {
	value := o.spring.Value()
	if value < 0.0 {
		return 0.0
	}
	if value > 1.0 {
		return 1.0
	}
	return value
}

// IsActive returns true if opacity is animating.
func (o *OpacitySpring) IsActive() bool {
	return o.spring.IsActive()
}

// IsVisible returns true if opacity > 0.01.
func (o *OpacitySpring) IsVisible() bool {
	return o.Opacity() > 0.01
}
