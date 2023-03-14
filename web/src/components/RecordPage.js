import React from 'react';
import data from '../data.js';
import image from '../image.js';
import Figure1 from '../Figure-1.png';

export default function RecordPage() {
  const [isPromptText, setIsPromptText] = React.useState(true);
  const initialPromptNum = 0;
  const [item, setItem] = React.useState(data[initialPromptNum]);
  const isRecorded = false;
  const [imagePath, setImagePath] = React.useState('');
  const totalPromptNum = data.length + image.length;

  function handleSkip() {
    if (item.promptNum < data.length - 1) {
      setItem((prevItem) => {
        return data[prevItem.promptNum + 1];
      });
    } else {
      setIsPromptText((prevIsText) => !prevIsText);
    }
  }

  return (
    <div className='record-page-container'>
      <div className='prompt-info-container'>
        <p className='propmt-sequential-number'>
          Prompt Number: {item.promptNum + 1}/{totalPromptNum}
        </p>
        <p className='prompt-section-name'>Section: {item.section}</p>
      </div>
      <div className='prompt-and-button-container'>
        {isPromptText ? (
          <div
            className='prompt-text-parent'
            style={{ height: '300px', overflowY: 'scroll' }}
          >
            <p className='prompt-text'>{item.prompt}</p>
          </div>
        ) : (
          <div>
            <p>Tell me what is happening in this picture</p>
            <img src={Figure1} alt='kitchen' className='image' />
          </div>
        )}
        <div className='prompt-button'>
          <button id='play' disabled={!isRecorded}>
            Play
          </button>
          <button id='discard' disabled={!isRecorded}>
            Discard
          </button>
        </div>
      </div>
      <div className='button-container'>
        <button id='shortcuts'>Shortcuts</button>
        <button id='record'>Record</button>
        <button id='skip' onClick={handleSkip}>
          Skip
        </button>
        <button id='submit'>Submit</button>
      </div>
    </div>
  );
}
