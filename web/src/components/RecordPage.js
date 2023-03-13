export default function RecordPage() {
  let currentPromptNumber = 1;
  const totalPromptNumber = 100;
  let currentPromptSectionName = 'words';
  let prompt =
    'Britney bought the ABBA album and grabbed banana bread for her lab in November.My mom climbed Burnaby Mountain from the bottom in thirty minutes.';
  return (
    <div>
      <div className='prompt-info-container'>
        <p className='propmt-sequencial-number'>
          Prompt Number: {currentPromptNumber}/{totalPromptNumber}
        </p>
        <p className='prompt-section-name'>
          Section: {currentPromptSectionName}
        </p>
      </div>
      <div className='prompt-and-button-container'>
        <div className='prompt-text'>{prompt}</div>
        <div className='prompt-button'>
          <button id='play'>Play</button>
          <button id='discard'>Discard</button>
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
