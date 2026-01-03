import React from 'react';
import '@testing-library/jest-dom/extend-expect';
import { render, fireEvent, screen } from '@testing-library/react';
import { NumpadInput } from '../../src/components/NumpadInput';

// Mock the playSound utility
jest.mock('../../src/util/util', () => ({
  playSound: jest.fn(),
}));

describe('NumpadInput', () => {
  it('renders correctly with initial value', () => {
    const onChange = jest.fn();
    render(<NumpadInput value="10" onChange={onChange} label="Test Label" />);
    
    expect(screen.getByText('10')).toBeInTheDocument();
    expect(screen.getByText('Test Label')).toBeInTheDocument();
  });

  it('calls onChange when input changes', () => {
    const onChange = jest.fn();
    render(<NumpadInput value="10" onChange={onChange} label="Test Label" />);
    
    const button = screen.getByText('5');
    fireEvent.click(button);
    
    // Check if called with the new number value
    expect(onChange).toHaveBeenCalledWith('105');
  });
});
