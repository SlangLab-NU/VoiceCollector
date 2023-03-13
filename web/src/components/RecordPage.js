import data from '../data.js';

export default function RecordPage() {
  let isPromptText = true;
  let i = 4;
  let item = data[i];
  let currentPromptNumber = item.promptNum;
  const totalPromptNumber = data.length;
  let currentPromptSectionName = item.section;
  let prompt = item.prompt;
  let isRecorded = false;

  return (
    <div className='record-page-container'>
      <div className='prompt-info-container'>
        <p className='propmt-sequential-number'>
          Prompt Number: {currentPromptNumber}/{totalPromptNumber}
        </p>
        <p className='prompt-section-name'>
          Section: {currentPromptSectionName}
        </p>
      </div>
      <div className='prompt-and-button-container'>
        {isPromptText ? (
          <div
            className='prompt-text-parent'
            style={{ height: '300px', overflowY: 'scroll' }}
          >
            <p className='prompt-text'>{prompt}</p>
          </div>
        ) : (
          <div>Image goes here</div>
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
        <button id='skip'>Skip</button>
        <button id='submit'>Submit</button>
      </div>
    </div>
  );
}
