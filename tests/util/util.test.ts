import { playSound } from '../../src/util/util';

describe('Utility Functions', () => {
  describe('playSound', () => {
    it('should play the audio', () => {
      const playMock = jest.fn();
      
      // Mock the Audio constructor
      global.Audio = jest.fn().mockImplementation(() => ({
        play: playMock,
      }));

      playSound('test-sound.wav');
      
      expect(global.Audio).toHaveBeenCalledWith('test-sound.wav');
      expect(playMock).toHaveBeenCalled();
    });
  });
});