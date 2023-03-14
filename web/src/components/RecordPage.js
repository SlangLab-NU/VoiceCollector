import React from 'react';
import data from '../data.js';

export default function RecordPage() {
  const initialPromptNum = 0;
  const [item, setItem] = React.useState(data[initialPromptNum]);
  const isRecorded = false;

  function handleSkip() {
    if (item.promptNum < data.length - 1) {
      setItem((prevItem) => {
        return data[prevItem.promptNum + 1];
      });
    } else {
      // hit the end of prompts
    }
  }

  return (
    <div className='record-page-container'>
      <div className='prompt-info-container'>
        <p className='propmt-sequential-number'>
          Prompt Number: {item.promptNum + 1}/{data.length}
        </p>
        <p className='prompt-section-name'>Section: {item.section}</p>
      </div>
      <div className='prompt-and-button-container'>
        {item.section !== 'Image' ? (
          <div
            className='prompt-text-parent'
            style={{ height: '500px', overflowY: 'scroll' }}
          >
            <p className='prompt-text'>{item.prompt}</p>
          </div>
        ) : (
          <div>
            <p>Tell me what is happening in this picture</p>
            <img src={`/assets/${item.prompt}`} alt='' className='image' />
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
        <button id='submit' disabled={!isRecorded}>
          Submit
        </button>
      </div>
    </div>
  );
}
