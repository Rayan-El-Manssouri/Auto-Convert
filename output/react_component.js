
import React from 'react';
import { PDFViewer, Document, Page, Text } from '@react-pdf/renderer';
import { Font } from '@react-pdf/renderer';
import PdfCustomView from './PdfCustomView';
import PdfText from './PdfText';

Font.register({ family: 'Helvetica-Compressed', src: './ttf/Helvetica-Compressed-Regular.ttf' });
Font.register({ family: 'TimesNewRomanPS-BoldItalicMT', src: './ttf/TimesNewRomanBoldItalic.ttf' });
Font.register({ family: 'Arial-BoldMT', src: './ttf/Arial-BoldMT.ttf' });
Font.register({ family: 'Helvetica-Black', src: './ttf/Helvetica-Black.ttf' });
Font.register({ family: 'Webdings', src: './ttf/Webdings.ttf' });
Font.register({ family: 'Helvetica-Condensed-Bold', src: './ttf/Helvetica-Condensed-Bold.ttf' });
Font.register({ family: 'Helvetica-Narrow', src: './ttf/Helvetica-Narrow.ttf' });
Font.register({ family: 'SourceSansPro-Semibold', src: './ttf/SourceSansPro-SemiBold.ttf' });
Font.register({ family: 'SourceSansPro-Bold', src: './ttf/SourceSansPro-Bold.ttf' });
Font.register({ family: 'Wingdings-Regular', src: './ttf/Wingdings-Regular.ttf' });
Font.register({ family: 'Helvetica-Narrow-Bold', src: './ttf/Helvetica-Narrow-Bold.ttf' });

const PdfComponent = () => (
    <PDFViewer style={ {  width: '100%', height: '100vh', border: 'none', position: 'fixed' }  }>
        <Document>
        <Page size="A4">
            <PdfText />
            <PdfCustomView />
        </Page>
        </Document>
    </PDFViewer>
);

export default PdfComponent;
